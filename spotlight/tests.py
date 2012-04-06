SKIP_ORDERED_DICT_TESTS = False
try:
    from collections import OrderedDict
except ImportError:
    SKIP_ORDERED_DICT_TESTS = True
    import sys
    sys.stderr.write('Skipping _dict_cleanup due to OrderedDict not being available.\n')

from nose.tools import eq_

from spotlight import _convert_number, _dict_cleanup


def test_number_convert():
    eq_(_convert_number('0'), 0)
    eq_(_convert_number('0.2'), 0.2)
    eq_(_convert_number(True), True)
    eq_(_convert_number('evi'), 'evi')


if not SKIP_ORDERED_DICT_TESTS:
    def test_dict_key_cleanup():
        dirty_dict = OrderedDict()
        dirty_dict['@dirty'] = 'value'
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
        eq_(_dict_cleanup(dirty_dict, dict_type=OrderedDict), clean_dict)
