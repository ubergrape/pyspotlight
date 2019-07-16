from collections import namedtuple, OrderedDict
from nose2.tools.such import helper
import spotlight


# Expose unittest assertions to function-style tests
assert_equals = helper.assertEquals
assert_raises = helper.assertRaises


def fake_request_post(self, *args, **kwargs):
    RawResponse = namedtuple('RawResponse', ['reason', ])
    hear_me_RawR = RawResponse(reason='Just a fake reason.')

    class FakeResponse(spotlight.requests.models.Response):
        content = kwargs['headers']['fake_response']

        def raise_for_status(self):
            self.raw = hear_me_RawR
            self.status_code = (kwargs['headers']['fake_status']
                                if 'fake_status' in kwargs['headers']
                                else spotlight.requests.codes.ok)
            return super(FakeResponse, self).raise_for_status()
    return FakeResponse()
spotlight.requests.post = fake_request_post


def test_number_convert():
    assert_equals(spotlight._convert_number('0'), 0)
    assert_equals(spotlight._convert_number('0.2'), 0.2)
    assert_equals(spotlight._convert_number(True), True)
    assert_equals(spotlight._convert_number('evi'), 'evi')
    # Testing the footnote workaround.
    assert_equals(spotlight._convert_number([1]), '[1]')


def test_protocol_missing():
    with assert_raises(spotlight.SpotlightException):
        spotlight.annotate('localhost', 'asdasdasd',
                           headers={'fake_response': b'invalid json',
                                    'fake_status': 502})


def test_http_fail():
    with assert_raises(spotlight.requests.exceptions.HTTPError):
        spotlight.annotate('http://localhost', 'asdasdasd',
                           headers={'fake_response': b'invalid json',
                                    'fake_status': 502})


def test_annotation_invalid_json():
    with assert_raises(ValueError):
        spotlight.annotate('http://localhost', 'asdasdasd',
                           headers={'fake_response': b'invalid json'})


def test_missing_resources():
    with assert_raises(spotlight.SpotlightException):
        spotlight.annotate('http://localhost', 'asdasdasd',
                           headers={'fake_response': b'{"Test": "Win"}'})


def test_candidates_invalid_json():
    with assert_raises(ValueError):
        spotlight.annotate('http://localhost', 'asdasdasd',
                           headers={'fake_response': b'invalid json'})


def test_missing_annotation():
    with assert_raises(spotlight.SpotlightException):
        spotlight.candidates('http://localhost', 'asdasdasd',
                             headers={'fake_response': b'{"Test": "Win"}'})


def test_missing_surfaceForms():
    with assert_raises(spotlight.SpotlightException):
        spotlight.candidates('http://localhost', 'asdasdasd',
                             headers={'fake_response': b'{"annotation": {"Test": "Win"}}'})


def test_single_candidate():
    # Test with a single returned candidate, as was reported by issue #3.
    # Thanks to aolieman for the awesome test data!
    data = b"""
{
   "annotation":{
      "@text":"Industrial Design at the Technische Universiteit Delft",
      "surfaceForm":{
         "@name":"Technische Universiteit Delft",
         "@offset":"25",
         "resource":[
            {
               "@label":"Technische Universiteit Delft",
               "@uri":"Technische_Universiteit_Delft",
               "@contextualScore":"0.9991813164782087",
               "@percentageOfSecondRank":"0.1422872887244497",
               "@support":"3",
               "@priorScore":"2.8799662606192636E-8",
               "@finalScore":"0.8754365122251001",
               "@types":""
            },
            {
               "@label":"Delft University of Technology",
               "@uri":"Delft_University_of_Technology",
               "@contextualScore":"8.186418452925803E-4",
               "@percentageOfSecondRank":"0.0",
               "@support":"521",
               "@priorScore":"5.001541405942121E-6",
               "@finalScore":"0.12456348777489806",
               "@types":"DBpedia:Agent, Schema:Organization, DBpedia:Organisation, Schema:EducationalOrganization, DBpedia:EducationalInstitution, Schema:CollegeOrUniversity, DBpedia:University"
            }
         ]
      }
   }
}
    """
    candidates = spotlight.candidates('http://localhost', 'asdasdasd',
                                      headers={'fake_response': data})
    expected_out = [
        {
            'resource': [
                {
                    'finalScore': 0.8754365122251001,
                    'support': 3,
                    'uri': 'Technische_Universiteit_Delft',
                    'label': 'Technische Universiteit Delft',
                    'types': '',
                    'percentageOfSecondRank': 0.1422872887244497,
                    'priorScore': 2.8799662606192636e-08,
                    'contextualScore': 0.9991813164782087
                },
                {
                    'finalScore': 0.12456348777489806,
                    'support': 521,
                    'uri': 'Delft_University_of_Technology',
                    'label': 'Delft University of Technology',
                    'types': 'DBpedia:Agent, Schema:Organization, DBpedia:Organisation, Schema:EducationalOrganization, DBpedia:EducationalInstitution, Schema:CollegeOrUniversity, DBpedia:University',
                    'percentageOfSecondRank': 0.0,
                    'priorScore': 5.001541405942121e-06,
                    'contextualScore': 0.0008186418452925803
                },
            ],
            'name': 'Technische Universiteit Delft',
            'offset': 25
        }
    ]
    assert_equals(candidates, expected_out)


def test_dict_key_cleanup():
    dirty_dict = OrderedDict()
    dirty_dict['@dirty'] = 'value'
    dirty_dict['@empty'] = None  # None values should be removed.
    dirty_dict['@recursive'] = OrderedDict()
    dirty_dict['@recursive']['tests'] = '1'
    dirty_dict['@recursive']['surfaceForm'] = '02'
    dirty_dict['@recursive']['name'] = '02'
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
    clean_dict['recursive']['surfaceForm'] = '02'
    clean_dict['recursive']['name'] = '02'
    clean_dict['recursive']['stuff'] = OrderedDict()
    more = OrderedDict()
    more['something'] = 'isgoingon'
    moremore = OrderedDict()
    moremore['moar'] = True
    moar_iterable = [more, moremore]
    clean_dict['recursive']['stuff'] = moar_iterable
    assert_equals(spotlight._dict_cleanup(dirty_dict, dict_type=OrderedDict), clean_dict)
