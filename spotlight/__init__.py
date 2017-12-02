"""
Python DBpedia Spotlight API Wrapper
====================================

This is just a simple interface to a Spotlight API.

Tested with DBPedia Spotlight 0.7.
"""
__version_info__ = (0, 7, 1)
__version__ = '.'.join(map(str, __version_info__))
__url__ = 'https://github.com/aolieman/pyspotlight'


import requests


class SpotlightException(Exception):
    """
    Exception raised on Spotlight failures.

    Basically this exception is raised if there was no valid JSON response
    from Spotlight.
    """
    pass


# Some helper functions.

def _post_request(address, payload, filters, headers):
    """
    Build the Spotlight request, POST it to the server, and return
    the response's JSON body.
    """
    filter_kwargs = {'policy': 'whitelist'}
    filter_kwargs.update(filters or {})
    payload.update(filter_kwargs)

    reqheaders = {'accept': 'application/json'}
    reqheaders.update(headers or {})

    # Its better for the user to have to explicitly provide a protocol in the
    # URL, since transmissions might happen over HTTPS or any other secure or
    # faster (spdy/HTTP2 :D) channel.
    if '://' not in address:
        raise SpotlightException('Oops. Looks like you forgot the protocol '
                                 '(http/https) in your url (%s).' % address)

    response = requests.post(address, data=payload, headers=reqheaders)

    # http status codes >=400,<600 shall raise an exception.
    response.raise_for_status()

    json_body = response.json()
    if json_body is None:
        raise SpotlightException("Spotlight's response did not contain valid "
                                 "JSON: %s" % response.text)

    return json_body


def _convert_number(value):
    """
    Try to convert a string to an int or float.
    """
    if isinstance(value, bool):
        return value
    # Workaround for footnotes being put into Resources.surfaceForm and then
    # having them parsed by the JSON parser into a list. (issue #4)
    if isinstance(value, list):
        value = str(value)

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
    for key, value in dic.items():
        if value is None:
            continue

        key = key.replace('@', '')
        try:
            try:
                # If this is a string or bool,
                # go straight to type conversion.
                if (hasattr(value, 'strip') or
                        isinstance(value, bool)):
                    raise AttributeError
                # Test for an iterable (list, tuple, set)
                value[0]
                # Clean up each element in the iterable
                clean[key] = [
                    _dict_cleanup(element, dict_type)
                    for element in value
                ]
            except KeyError:
                clean[key] = _dict_cleanup(value, dict_type)
        except AttributeError:
            if key in {'surfaceForm', 'name'}:
                clean[key] = value
            else:
                clean[key] = _convert_number(value)
    return clean


# Main functions.

def annotate(address, text, confidence=0.0, support=0,
             spotter='Default', disambiguator='Default',
             filters=None, headers=None):
    """
    Get semantic annotations (i.e. entity links) from a text.

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
        Only output annotations above a given prominence (i.e. support,
        indegree on Wikipedia).
    :type support: integer

    :param spotter:
        One of spotters available on your DBPedia Spotlight server.
        For example one of: LingPipeSpotter, AtLeastOneNounSelector,
                            CoOccurrenceBasedSelector
    :type spotter: string

    :param disambiguator:
        The disambiguator to use on the annotation.
    :type disambiguator: string

    :param filters:
        Additional parameters that collectively define a filter function.

        For example:
        'policy'                (string)
                                The policy to be used:
                                'whitelist' or 'blacklist';
        'types'                 (string)
                                Comma-separated list of types,
                                i.e. 'DBpedia:Agent,Schema:Organization';
        'sparql'                (string)
                                Select only entities that (don't)
                                match with the SPARQL query result;
        'coreferenceResolution' (boolean)
                                Annotate coreferences: true / false.
                                Set to false to use types (statistical only).

    :type filters: dictionary

    :param headers:
        Additional headers to be set on the request.
    :type headers: dictionary

    :rtype: list of resources
    """
    payload = {
        'confidence': confidence,
        'support': support,
        'text': text,
        'spotter': spotter,
        'disambiguator': disambiguator
    }

    pydict = _post_request(address, payload, filters, headers)

    if 'Resources' not in pydict:
        raise SpotlightException(
            'No Resources found in spotlight response: %s' % pydict
        )

    return [_dict_cleanup(resource) for resource in pydict['Resources']]


def candidates(address, text, confidence=0.0, support=0,
               spotter='Default', disambiguator='Default',
               filters=None, headers=None):
    """
    Get the candidate entities from a text.

    Uses the same arguments as :meth:`annotate`.

    :rtype: list of surface forms
    """
    payload = {
        'confidence': confidence,
        'support': support,
        'text': text,
        'spotter': spotter,
        'disambiguator': disambiguator
    }

    pydict = _post_request(address, payload, filters, headers)

    if 'annotation' not in pydict:
        raise SpotlightException(
            'No annotations found in spotlight response: %s' % pydict
        )
    if 'surfaceForm' not in pydict['annotation']:
        raise SpotlightException(
            'No surface forms found in spotlight response: %s' % pydict
        )

    # Previously we assumed that the surfaceForm is *always* a list, however
    # depending on how many are returned, this does not have to be the case.
    # So we are doing some good ol' duck typing here.
    try:
        pydict['annotation']['surfaceForm'][0]
    except KeyError:
        # However note that we will *always* return a list.
        return [_dict_cleanup(pydict['annotation']['surfaceForm']), ]
    return [
        _dict_cleanup(form)
        for form in pydict['annotation']['surfaceForm']
    ]
