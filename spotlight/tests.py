SKIP_ORDERED_DICT_TESTS = False
try:
    from collections import OrderedDict
except ImportError:
    SKIP_ORDERED_DICT_TESTS = True
    import sys
    sys.stderr.write('Skipping _dict_cleanup due to OrderedDict not being '
                     'available.\n')

from nose.tools import eq_, nottest, raises

import spotlight


@nottest
def fake_request_post(self, *args, **kwargs):
    class FakeResponse(object):
        text = kwargs['headers']['fake_response']
    return FakeResponse()
spotlight.requests.post = fake_request_post


def test_number_convert():
    eq_(spotlight._convert_number('0'), 0)
    eq_(spotlight._convert_number('0.2'), 0.2)
    eq_(spotlight._convert_number(True), True)
    eq_(spotlight._convert_number('evi'), 'evi')


@raises(spotlight.SpotlightException)
def test_annotation_invalid_json():
    spotlight.annotate('localhost', 'asdasdasd',
                       headers={'fake_response': 'invalid json'})


@raises(spotlight.SpotlightException)
def test_missing_resources():
    spotlight.annotate('localhost', 'asdasdasd',
            headers={'fake_response': '{"Test": "Win"}'})


@raises(spotlight.SpotlightException)
def test_candidates_invalid_json():
    spotlight.annotate('localhost', 'asdasdasd',
                       headers={'fake_response': 'invalid json'})


@raises(spotlight.SpotlightException)
def test_missing_annotation():
    spotlight.candidates('localhost', 'asdasdasd',
            headers={'fake_response': '{"Test": "Win"}'})


@raises(spotlight.SpotlightException)
def test_missing_surfaceForms():
    spotlight.candidates('localhost', 'asdasdasd',
            headers={'fake_response': '{"annotation": {"Test": "Win"}}'})


if not SKIP_ORDERED_DICT_TESTS:
    def test_dict_key_cleanup():
        dirty_dict = OrderedDict()
        dirty_dict['@dirty'] = 'value'
        dirty_dict['@empty'] = None  # None values should be removed.
        dirty_dict['@recursive'] = OrderedDict()
        dirty_dict['@recursive']['tests'] = '1'
        dirty_dict['@recursive']['stuff'] = OrderedDict()
        more = OrderedDict()
        more['something'] = 'isgoingon'
        moremore = OrderedDict()
        moremore['@moar'] = True
        moar_iterable = [more, moremore]
        dirty_dict['@recursive']['stuff'] = moar_iterable

        clean_dict = OrderedDict()
        clean_dict['dirty'] = 'value'
        clean_dict['recursive'] = OrderedDict()
        clean_dict['recursive']['tests'] = 1
        clean_dict['recursive']['stuff'] = OrderedDict()
        more = OrderedDict()
        more['something'] = 'isgoingon'
        moremore = OrderedDict()
        moremore['moar'] = True
        moar_iterable = [more, moremore]
        clean_dict['recursive']['stuff'] = moar_iterable
        eq_(spotlight._dict_cleanup(dirty_dict, dict_type=OrderedDict),
            clean_dict)
