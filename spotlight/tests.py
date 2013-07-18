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
    # Testing the footnote workaround.
    eq_(spotlight._convert_number([1]), '[1]')


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


def test_single_candidate():
    # Test with a single returned candidate, as was reported by issue #3.
    # Thanks to aolieman for the awesome test data!
    data = """
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
        {u'resource':
            [
                {
                    u'finalScore': 0.8754365122251001,
                    u'support': 3,
                    u'uri': u'Technische_Universiteit_Delft',
                    u'label': u'Technische Universiteit Delft',
                    u'types': u'',
                    u'percentageOfSecondRank': 0.1422872887244497,
                    u'priorScore': 2.8799662606192636e-08,
                    u'contextualScore': 0.9991813164782087
                },
                {
                    u'finalScore': 0.12456348777489806,
                    u'support': 521,
                    u'uri': u'Delft_University_of_Technology',
                    u'label': u'Delft University of Technology',
                    u'types': u'DBpedia:Agent, Schema:Organization, DBpedia:Organisation, Schema:EducationalOrganization, DBpedia:EducationalInstitution, Schema:CollegeOrUniversity, DBpedia:University',
                    u'percentageOfSecondRank': 0.0,
                    u'priorScore': 5.001541405942121e-06,
                    u'contextualScore': 0.0008186418452925803
                },
             ],
         u'name': u'Technische Universiteit Delft',
         u'offset': 25
        }
    ]
    eq_(candidates, expected_out)


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
