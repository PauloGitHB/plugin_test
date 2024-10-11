import re
from typing import TYPE_CHECKING

import numpy as np
import os

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive,EntryMetadata
    from structlog.stdlib import BoundLogger

from nomad.config import config

from nomad.parsing.parser import MatchingParser

from plugin_test.schema_packages.waveform_package import (
    TemporalWaveform,
    Waveform,
    Oscilloscope
    )


configuration = config.get_plugin_entry_point(
    'plugin_test.parsers:parser_entry_point'
)

class OscilloscopeParser(MatchingParser):

    def parse(self,
              mainfile: str,
              archive: 'EntryArchive',
              logger: 'BoundLogger' = None,
              child_archives: dict[str, 'EntryArchive'] = None) -> None:

        if not mainfile or not os.path.exists(mainfile):
            return

        with open(mainfile) as file:
            lines = file.readlines()


        """parsing"""

        author = lines[0].strip()
        instrument = lines[1].strip()
        num_signals = int(re.search(r'\d+', lines[2]).group())
        num_points = int(re.search(r'\d+', lines[3]).group())
        delta_t = float(re.search(r'[\d.]+', lines[4]).group())

        """instanciation"""

        schema_instance = TemporalWaveform()
        schema_instance.author = author
        schema_instance.num_points = num_points
        schema_instance.delta_t = delta_t

        """instrument part"""


        oscilloscope = Oscilloscope()

        oscilloscope.n_channels = num_signals
        oscilloscope.name = instrument

        schema_instance.instruments = []
        schema_instance.instruments.append(oscilloscope)

        """channel part"""

        data_start_index = next(i for i, line in enumerate(lines)
                                if line.startswith('*')) + 1

        schema_instance.results = []

        for ind_channel in range(num_signals):

            channel_name = lines[data_start_index + 2 * ind_channel].strip().replace(":", "")

            signal_data = [float(val) for val in lines[data_start_index + 2 * ind_channel + 1].split(',')]

            waveform = Waveform()

            waveform.amplitude = np.array(signal_data)
            waveform.time =  np.arange(0, num_points * delta_t, delta_t)
            waveform.name = channel_name

            schema_instance.results.append(waveform)

        archive.data = schema_instance


    """fonction normalize"""

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:

        super().normalize(archive, logger)