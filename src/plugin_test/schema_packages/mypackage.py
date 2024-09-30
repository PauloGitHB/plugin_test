from nomad.metainfo import Quantity, MSection, SubSection, MEnum, MCategory, Section
from nomad.datamodel.data import Schema
from nomad.metainfo.metainfo import MSection, Quantity, SubSection
from nomad.config import config

configuration = config.get_plugin_entry_point(
    'plugin_test.schema_packages:schema_package_entry_point'
)

m_package = Schema()

class Metadata(MSection):
    author = Quantity(type=str, description='Author of the file')
    instrument = Quantity(type=str, description='Type of instrument used')
    n_signals = Quantity(type=int, description='Number of signals')
    n_points = Quantity(type=int, description='Number of data points')

class Signal(MSection):
    name = Quantity(type=str, description='Name of the signal (e.g., CH1, CH2)')
    data = Quantity(type=float, shape=['*'], description='Data points for the signal')

class Experiment(MSection):
    metadata = SubSection(sub_section=Metadata, description='Metadata for the experiment')
    signals = SubSection(sub_section=Signal, repeats=True, description='List of signals')

m_package.__init_metainfo__()