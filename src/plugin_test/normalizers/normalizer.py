from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    pass

from nomad.config import config
from nomad.normalizing import Normalizer

configuration = config.get_plugin_entry_point(
    'plugin_test.normalizers:normalizer_entry_point'
)

class MyNormalizer(Normalizer):
    def normalize(self, archive, logger):
        logger.info('Normalizing data')

        if not archive.metadata.instrument:
            archive.metadata.instrument = 'Unknown Instrument'
            logger.warning('Instrument not provided, set to "Unknown Instrument".')

        for signal in archive.signals:
            if not hasattr(signal, 'unit'):
                signal.unit = 'arbitrary_unit'
                logger.info(f'Unit for {signal.name} set to "arbitrary_unit"')

s