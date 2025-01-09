from plugin_test.parsers.parser import InstrumentParser
from plugin_test.schema_packages.waveform_package import TemporalWaveform
import os
import logging
import json

def test_parser():
    parser = InstrumentParser()
    schema_instance = TemporalWaveform()

    test_file = os.path.join(os.path.dirname(__file__), '../data/data.txt')
    parser.parse(test_file,schema_instance,logging.getLogger(__name__), None)

    json_res = json.dumps(schema_instance.to_dict(), indent=4)
    print(json_res)

test_parser()