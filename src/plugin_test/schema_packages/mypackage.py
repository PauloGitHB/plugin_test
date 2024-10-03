from typing import (
     TYPE_CHECKING,
 )

import numpy as np
from nomad.config import config
from nomad.datamodel.data import Schema,EntryData
from nomad.datamodel.metainfo.basesections import Instrument,Measurement, ArchiveSection
from nomad.metainfo import Quantity, SchemaPackage

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

configuration = config.get_plugin_entry_point(
    'plugin_test.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()


class TemporalWaveform(Measurement,Instrument,EntryData):

    data_file = Quantity(
        type=str,
        description='The recipe file for the sintering process.',
        a_eln={
            "component": "FileEditQuantity",
        },
    )

    author = Quantity(
        type=str,
        description='The name of the author of the data file'
    )

    num_signals = Quantity(
        type=int,
        description='the number of signals for this experience'
    )

    num_points = Quantity(
        type=int,
        description='The number of points'
    )

    delta_t = Quantity(
        type=np.float64,
        description='the delta of time for this experience'
    )

    signals = Quantity(
        type = np.float64,
        shape = ['num_signals','num_points'],
        description='the storage of all the signals'
    )

    # def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:

    #      super().normalize(archive, logger)

   # measurement = SubSection(section_def=Measurement,repeats=False)



m_package.__init_metainfo__()
