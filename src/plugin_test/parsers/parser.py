import re
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

from nomad.config import config
from nomad.parsing.parser import MatchingParser

from plugin_test.schema_packages.waveform_package import TemporalWaveform, Waveform

configuration = config.get_plugin_entry_point(
    'plugin_test.parsers:parser_entry_point'
)


class OscilloscopeParser(MatchingParser):

    def parse(self,
              mainfile: str,
              archive: 'EntryArchive',
              logger: 'BoundLogger' = None,
              child_archives: dict[str, 'EntryArchive'] = None) -> None:
        with open(mainfile) as file:
            lines = file.readlines()

        schema_instance = TemporalWaveform()
        schema_instance.results = Waveform()

        author = lines[0].strip()
        instrument = lines[1].strip()
        num_signals = int(re.search(r'\d+', lines[2]).group())
        num_points = int(re.search(r'\d+', lines[3]).group())
        delta_t = float(re.search(r'[\d.]+', lines[4]).group())

        schema_instance.author = author

        # instrument_object = InstrumentReference()
        # instrument_object.name = instrument

        # if archive.results.eln.instruments is None:
        #     archive.results.eln.instruments =[]
        # archive.results.eln.instruments.append(instrument_object)

        schema_instance.instrument = instrument

        schema_instance.num_signals = num_signals
        schema_instance.num_points = num_points
        schema_instance.delta_t = delta_t

        data_start_index = next(i for i, line in enumerate(lines)
                                if line.startswith('*')) + 1


        schema_instance.results.amplitude = np.zeros(num_points)
        schema_instance.results.time = np.zeros(num_points)

        for i in range(num_signals):
            signal_data = [float(val) for val in lines[data_start_index + 2 * i + 1].split(',')]

            if i == 0:
                schema_instance.results.amplitude = np.array(signal_data)
            elif i == 1:
                schema_instance.results.time = np.array(signal_data)

        schema_instance.results.name = "result"

        archive.data = schema_instance

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:

        super().normalize(archive, logger)