import numpy as np
from nomad.config import config
from nomad.datamodel.data import Schema
from nomad.datamodel.metainfo.basesections import Instrument, Measurement
from nomad.metainfo import Quantity, SchemaPackage

configuration = config.get_plugin_entry_point(
    'plugin_test.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()


class TemporalWaveform(Schema,Measurement,Instrument):
    author = Quantity(
        type=str,
        description='The name of the author of the data file'
    )

    instrument = Quantity(
        type=str,
        description='the instrument we used for this experience'
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

   # measurement = SubSection(section_def=Measurement,repeats=False)



m_package.__init_metainfo__()
