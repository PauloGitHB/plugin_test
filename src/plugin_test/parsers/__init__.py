from nomad.config.models.plugins import ParserEntryPoint
from pydantic import Field


class MyParserEntryPoint(ParserEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from plugin_test.parsers.parser import MyParser

        return MyParser(**self.dict())


parser_entry_point = MyParserEntryPoint(
    name='MyParser',
    description='New parser entry point configuration.',
    mainfile_name_re='.*\.txt',
)
