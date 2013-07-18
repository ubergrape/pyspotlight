"""
Python DBpedia Spotlight API Wrapper
====================================

This is just a simple interface to a Spotlight API.

Tested with DBPedia Spotlight 0.5 and 0.6.5.

Note that I'm trying to track Spotlight release version numbers, so you can
easily see which pyspotlight version has been tested with which Spotlight
release.

I hope the code and the small documentation speaks for itself :-)

If you should encounter any problems, feel free to contact me on github
(originell). I'm happy to help out with anything related to my code.
"""
__version_info__ = (0, 6, 5)
__version__ = '.'.join(map(str, __version_info__))


import requests


class SpotlightException(Exception):
    """
    Exception raised on Spotlight failures.

    Basically this exception is raised if there was no valid JSON response
    from Spotlight.
    """
    pass


# Some helper functions.
def _convert_number(value):
    """
    Try to convert a string to an int or float.
    """
    if isinstance(value, bool):
        return value
    # Workaround for footnotes being put into Resources.surfaceForm and then
    # having them parsed by the JSON parser into a list. (issue #4)
    if isinstance(value, list):
        value = unicode(value)

    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def _dict_cleanup(dic, dict_type=dict):
    """
    Clean the response dictionary from ugly @ signs in keys.

    TODO: Make this an iteration based recursion instead of function based.
          That way we can avoid stack fails.
    """
    clean = dict_type()
    for key, value in dic.iteritems():
        if value is None:
            continue

        key = key.replace('@', '')
        try:
            try:
                # If this is a string or bool,
                # go straight to type conversion.
                if (isinstance(value, basestring) or
                        isinstance(value, bool)):
                    raise AttributeError
                # Test for an iterable (list, tuple, set)
                value[0]
                # Clean up each element in the iterable
                clean[key] = [_dict_cleanup(element, dict_type)
                                for element in value]
            except KeyError:
                clean[key] = _dict_cleanup(value, dict_type)
        except AttributeError:
            clean[key] = _convert_number(value)
    return clean


# Main functions.
#
# I was inspired to go back to a function based approach after seeing this
# awesome talk by Jack Diederich: Stop Writing Classes
# http://pyvideo.org/video/880/stop-writing-classes
# Most of the class-based approach had the problems he described.
# Embarrassing!
def annotate(address, text, confidence=0.0, support=0,
             spotter='LingPipeSpotter', disambiguator='Default',
             policy='whitelist', headers={}):
    """
    Annotate a text.

    Can raise :exc:`requests.exceptions.HTTPError` or
    :exc:`SpotlightException`, depending on where the failure is (HTTP status
    code not 200 or the response not containing valid json).

    :param address:
        The absolute address of the annotate REST API.
    :type address: string

    :param text:
        The text to be sent.
    :type text: string

    :param confidence:
        Filter out annotations below a given confidence.
        Based on my experience I would suggest you set this to something
        above 0.4, however your experience might vary from text to text.
    :type confidence: float

    :param support:
        Only output annotations above a given prominence (support).
        Based on my experience I would suggest you set this to something
        above 20, however your experience might vary from text to text.
    :type support: int

    :param spotter:
        One of spotters available on your DBPedia Spotlight server.
        For example one of: LingPipeSpotter, AtLeastOneNounSelector,
                            CoOccurrenceBasedSelector
    :type spotter: string

    :param disambiguator:
        The disambiguator to use on the annotation.
    :type disambiguator: string

    :param policy:
        The policy to be used.
    :type disambiguator: string

    :param headers:
        Additional headers to be set on the request.
    :type headers: dictionary

    :rtype: list of resources
    """
    payload = {'confidence': confidence, 'support': support,
               'spotter': spotter, 'disambiguator': disambiguator,
               'policy': policy, 'text': text}
    reqheaders = {'accept': 'application/json'}
    reqheaders.update(headers)

    # Its better for the user to have to explicitly provide a protocl in the
    # URL, since transmissions might happen over HTTPS or any other secure or
    # faster (spdy :D) channel.
    if not '://' in address:
        raise SpotlightException('Oops. Looks like you forgot the protocol '
                                 '(http/https) in your url (%s).' % address)

    response = requests.post(address, data=payload, headers=reqheaders)
    if response.status_code != requests.codes.ok:
        # Every http code besides 200 shall raise an exception.
        response.raise_for_status()

    pydict = response.json
    if pydict is None:
        raise SpotlightException("Spotlight's response did not contain valid "
                                 "JSON: %s" % response.text)

    if not 'Resources' in pydict:
        raise SpotlightException(
                'No Resources found in spotlight response: %s' % pydict)

    return [_dict_cleanup(resource) for resource in pydict['Resources']]


# This is more or less a duplicate of the annotate function, with just
# the return line being the difference haha.
def candidates(address, text, confidence=0.0, support=0,
             spotter='LingPipeSpotter', disambiguator='Default',
             policy='whitelist', headers={}):
    """
    Get the candidates from a text.

    Uses the same arguments as :meth:`annotate`.

    :rtype: list of surface forms
    """
    payload = {'confidence': confidence, 'support': support,
               'spotter': spotter, 'disambiguator': disambiguator,
               'policy': policy, 'text': text}
    reqheaders = {'accept': 'application/json'}
    reqheaders.update(headers)
    response = requests.post(address, data=payload, headers=reqheaders)
    if response.status_code != requests.codes.ok:
        # Every http code besides 200 shall raise an exception.
        response.raise_for_status()

    pydict = response.json
    if pydict is None:
        raise SpotlightException("Spotlight's response did not contain valid "
                                 "JSON: %s" % response.text)

    if not 'annotation' in pydict:
        raise SpotlightException(
                'No annotations found in spotlight response: %s' % pydict)
    if not 'surfaceForm' in pydict['annotation']:
        raise SpotlightException(
                'No surface forms found in spotlight response: %s' % pydict)

    # Previously we assumed that the surfaceForm is *always* a list, however
    # depending on how many are returned, this does not have to be the case.
    # So we are doing some good ol' duck typing here.
    try:
        pydict['annotation']['surfaceForm'][0]
    except KeyError:
        # However note that we will *always* return a list.
        return [_dict_cleanup(pydict['annotation']['surfaceForm']), ]
    return [_dict_cleanup(form)
            for form in pydict['annotation']['surfaceForm']]
