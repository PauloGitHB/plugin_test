import re
from typing import (
    TYPE_CHECKING,
)

import numpy as np
from nomad.datamodel.data import (
    ArchiveSection,
    EntryData,
)
from nomad.datamodel.metainfo.basesections import Measurement, MeasurementResult
from nomad.metainfo import (
    Quantity,
    SchemaPackage,
    Section,
    SubSection,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

    from plugin_test.parsers.parser import OscilloscopeParser


m_package = SchemaPackage()


class Waveform(MeasurementResult, ArchiveSection):
    amplitude= Quantity(
        type=float,
        shape=['*'],
        description="the amplitude of the channel",
        unit="volt"
    )
    time=Quantity(
        type=float,
        shape=['*'],
        description='the time of the channel',
        unit='second'
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

    instrument = Quantity(
        type=str,
        description='the instrument used in this experience'
    )

    num_signals = Quantity(
        type=int,
        description='the number of signals for this experience',
         a_eln={
            "component": "NumberEditQuantity"
        }
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
        repeats=False,
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
            parser = OscilloscopeParser()
            parser.parse(self.data_file,archive,logger)

            with open(self.data_file) as file:
                lines = file.readlines()
            step = TemporalWaveform()
            step.author = lines[0].strip()
            step.instrument = lines[1].strip()
            step.num_signals = int(re.search(r'\d+', lines[2]).group())
            step.num_points = int(re.search(r'\d+', lines[3]).group())
            step.delta_t = float(re.search(r'[\d.]+', lines[4]).group())

            self.steps = step

m_package.__init_metainfo__()