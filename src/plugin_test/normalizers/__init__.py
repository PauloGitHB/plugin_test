from nomad.config.models.plugins import NormalizerEntryPoint
from pydantic import Field


class MyNormalizerEntryPoint(NormalizerEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from plugin_test.normalizers.normalizer import MyNormalizer

        return MyNormalizer(**self.dict())


normalizer_entry_point = MyNormalizerEntryPoint(
    name='MyNormalizer',
    description='New normalizer entry point configuration.',
)
