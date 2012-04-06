__version_info__ = (0, 5, 2)
__version__ = '.'.join(map(str, __version_info__))


try:
    import json
except ImportError:
    import simplejson as json

import requests


# Some helper functions.
def _convert_number(value):
    """
    Try to convert a string to an int or float.
    """
    if isinstance(value, bool): return value

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
    """
    clean = dict_type()
    for key, value in dic.iteritems():
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
    response = requests.post(address, data=payload, headers=reqheaders)
    pydict = json.loads(response.text)
    return [_dict_cleanup(resource) for resource in pydict['Resources']]


# This is more or less a duplicate of the annotate function, with just
# the return line being the difference haha.
def candidates(address, text, confidence=0.0, support=0,
             spotter='LingPipeSpotter', disambiguator='Default',
             policy='whitelist', headers={}):
    """
    Get the candidates from a text.

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

    :rtype: list of surface forms
    """
    payload = {'confidence': confidence, 'support': support,
               'spotter': spotter, 'disambiguator': disambiguator,
               'policy': policy, 'text': text}
    reqheaders = {'accept': 'application/json'}
    reqheaders.update(headers)
    response = requests.post(address, data=payload, headers=reqheaders)
    pydict = json.loads(response.text)
    return [_dict_cleanup(form)
            for form in pydict['annotation']['surfaceForm']]
