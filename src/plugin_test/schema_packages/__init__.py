from nomad.config.models.plugins import SchemaPackageEntryPoint
from pydantic import Field


class MySchemaPackageEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from plugin_test.schema_packages.mypackage import m_package

        return m_package


schema_package_entry_point = MySchemaPackageEntryPoint(
    name='MySchemaPackage',
    description='New schema package entry point configuration.',
)
