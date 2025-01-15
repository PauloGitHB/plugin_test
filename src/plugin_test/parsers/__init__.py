from nomad.config.models.plugins import ParserEntryPoint
from pydantic import Field


class OscilloscopeEntryPoint(ParserEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from plugin_test.parsers.parser import InstrumentParser

        return InstrumentParser(**self.dict())


parser_entry_point = OscilloscopeEntryPoint(
    name='MyParser',
    description='New parser entry point configuration.',
    mainfile_name_re='^.*\.data\.txt$',
)