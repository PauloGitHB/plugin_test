import re
from typing import (
    TYPE_CHECKING,
)

import numpy as np
from nomad.datamodel.data import (
    ArchiveSection,
    EntryData
)
from nomad.datamodel.metainfo.basesections import (
    Measurement,
    MeasurementResult,
    InstrumentReference,
    Instrument,
    ELNAnnotation)

from nomad.metainfo import (
    Quantity,
    SchemaPackage,
    Section,
    SubSection,
    MSection
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

    from plugin_test.parsers.parser import InstrumentParser


m_package = SchemaPackage()

class WaveformXCoordinate(MSection):
    name = Quantity(
        type = str,
        description = ""
    )

    unity = Quantity(
        type = str,
        description = ""
    )

    value = Quantity(
        type=float,
        shape=['*'],
        description="the amplitude of the channel",
        unit= 'second'
    )

class WaveformYCoordinate(MSection):
    name = Quantity(
        type = str,
        description = ""
    )

    unity = Quantity(
        type = str,
        description = ""
    )

    value = Quantity(
        type=float,
        shape=['*'],
        description="the amplitude of the channel",
        unit= 'volt'
    )


class Waveform(MeasurementResult):
    name = Quantity(
        type = str,
        description = ""
    )

    x_coordinate = SubSection(
        section_def = WaveformXCoordinate,
        description = "",
        repeats = False
    )

    y_coordinate = SubSection(
        section_def = WaveformYCoordinate,
        description = "",
        repeats = False
    )

class Oscilloscope(Instrument):
    n_channels = Quantity(
        type=int,
        description='the number of channels fon this Instrument',
         a_eln={
            "component": "NumberEditQuantity"
        }
    )


class OscilloscopeReference(InstrumentReference):
      reference = Quantity(
        type=Oscilloscope,
        description='A reference to a NOMAD `Instrument` entry.',
        a_eln=ELNAnnotation(
            component='ReferenceEditQuantity',
            label='instrument reference',
        ),
    )

class TemporalWaveform(Measurement, EntryData, ArchiveSection):
    m_def = Section(
        a_eln={
            "properties": {
                "order": [
                    "author",
                    "instrument",
                    "num_signals",
                    "num_points",
                    "delta_t",
                    "result"
                ]
            }
        },)


    author = Quantity(
        type=str,
        description='The author for this measurement',
    )

    instruments = SubSection(
        section_def = OscilloscopeReference,
        description="instrument used for this measurement",
        repeats=True,
    )

    num_points = Quantity(
        type=int,
        description='The number of points',
        a_eln={
            "component": "NumberEditQuantity"
        }
    )

    delta_t = Quantity(
        type=np.float64,
        description='the delta of time for this experience',
        a_eln={
            "component": "NumberEditQuantity"
        }
    )

    results = SubSection(
        section_def=Waveform,
        description="""
        The result of the measurement.
        """,
        repeats=True,
    )


    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:

        super().normalize(archive, logger)



class OscilloscopeMeasure(EntryData, ArchiveSection):
    m_def = Section()
    steps = SubSection(
        section_def=TemporalWaveform,
        repeats=True,
    )

    data_file = Quantity(
        type=str,
        description='The recipe.',
        a_eln={
            "component": "FileEditQuantity",
        },
    )

    def normalize(self, archive, logger: 'BoundLogger') -> None:
        '''
        The normalizer for the `Sintering` class.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        '''

        super(OscilloscopeMeasure, self).normalize(archive, logger)
        if self.data_file:
            parser = InstrumentParser()
            parser.parse(self.data_file,archive,logger)


            with open(self.data_file) as file:
                lines = file.readlines()

            steps = []

            step = TemporalWaveform()
            step.author = lines[0].strip()
            step.instrument.n_channel = int(re.search(r'\d+', lines[2]).group())
            step.num_points = int(re.search(r'\d+', lines[3]).group())
            step.delta_t = float(re.search(r'[\d.]+', lines[4]).group())
            steps.append(step)


        self.steps = step

m_package.__init_metainfo__()