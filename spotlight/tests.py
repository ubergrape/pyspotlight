SKIP_ORDERED_DICT_TESTS = False
try:
    from collections import OrderedDict
except ImportError:
    SKIP_ORDERED_DICT_TESTS = True
    import sys
    sys.stderr.write('Skipping _dict_cleanup due to OrderedDict not being '
                     'available.\n')

from collections import namedtuple
from nose.tools import eq_, nottest, raises

import spotlight


@nottest
def fake_request_post(self, *args, **kwargs):
    RawResponse = namedtuple('RawResponse', ['reason',])
    hear_me_RawR = RawResponse(reason='Just a fake reason.')

    class FakeResponse(spotlight.requests.models.Response):
        text = kwargs['headers']['fake_response']

        def raise_for_status(self):
            self.raw = hear_me_RawR
            self.status_code = (kwargs['headers']['fake_status']
                                if 'fake_status' in kwargs['headers']
                                else spotlight.requests.codes.ok)
            return super(FakeResponse, self).raise_for_status()
    return FakeResponse()
spotlight.requests.post = fake_request_post


def test_number_convert():
    eq_(spotlight._convert_number('0'), 0)
    eq_(spotlight._convert_number('0.2'), 0.2)
    eq_(spotlight._convert_number(True), True)
    eq_(spotlight._convert_number('evi'), 'evi')


@raises(spotlight.SpotlightException)
def test_protocol_missing():
    spotlight.annotate('localhost', 'asdasdasd',
                       headers={'fake_response': 'invalid json',
                                'fake_status': 502})


@raises(spotlight.requests.exceptions.HTTPError)
def test_http_fail():
    spotlight.annotate('http://localhost', 'asdasdasd',
                       headers={'fake_response': 'invalid json',
                                'fake_status': 502})


@raises(spotlight.SpotlightException)
def test_annotation_invalid_json():
    spotlight.annotate('http://localhost', 'asdasdasd',
                       headers={'fake_response': 'invalid json'})


@raises(spotlight.SpotlightException)
def test_missing_resources():
    spotlight.annotate('http://localhost', 'asdasdasd',
            headers={'fake_response': '{"Test": "Win"}'})


@raises(spotlight.SpotlightException)
def test_candidates_invalid_json():
    spotlight.annotate('http://localhost', 'asdasdasd',
                       headers={'fake_response': 'invalid json'})


@raises(spotlight.SpotlightException)
def test_missing_annotation():
    spotlight.candidates('http://localhost', 'asdasdasd',
            headers={'fake_response': '{"Test": "Win"}'})


@raises(spotlight.SpotlightException)
def test_missing_surfaceForms():
    spotlight.candidates('http://localhost', 'asdasdasd',
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
