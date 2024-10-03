import json
import logging
import os

from nomad.datamodel.datamodel import EntryArchive

from plugin_test.parsers.parser import MyParser


def test_parser():
    parser = MyParser()
    archive = EntryArchive()
    test_file = os.path.join(os.path.dirname(__file__),'../data/data.txt')


    parser.parse(test_file, archive, logging.getLogger(__name__),None)

    json_res = json.dumps(archive.data.m_to_dict(), indent=4)

    print(json_res)
test_parser()