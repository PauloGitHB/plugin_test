import re
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

from nomad.config import config
from nomad.parsing.parser import MatchingParser

from plugin_test.schema_packages.mypackage import TemporalWaveform

configuration = config.get_plugin_entry_point(
    'plugin_test.parsers:parser_entry_point'
)


class MyParser(MatchingParser):
    def __init__(self):
        super().__init__(
            mainfile_name_re=r'.*\.txt$',
            mainfile_mime_re=r'text/.*',
            mainfile_contents_re=r'.*',
        )

    def parse(self,
              mainfile: str,
              archive: 'EntryArchive',
              logger: 'BoundLogger' = None,
              child_archives: dict[str, 'EntryArchive'] = None) -> None:
        with open(mainfile) as file:
            lines = file.readlines()

        schema_instance = TemporalWaveform()

        author = lines[0].strip()
        instrument = lines[1].strip()
        num_signals = int(re.search(r'\d+', lines[2]).group())
        num_points = int(re.search(r'\d+', lines[3]).group())
        delta_t = float(re.search(r'[\d.]+', lines[4]).group())

        schema_instance.author = author
        schema_instance.instrument = instrument
        """schema_instance.instrument.name = instrument
        archive.results.eln.instruments.append(instrument)"""

        schema_instance.num_signals = num_signals
        schema_instance.num_points = num_points
        schema_instance.delta_t = delta_t

        schema_instance.results.name = "Here is a description of the results"

        data_start_index = next(i for i, line in enumerate(lines)
                                if line.startswith('*')) + 1


        """comment utiliser results"""

        schema_instance.signals = np.zeros((num_signals, num_points))

        for i in range(num_signals):
           # signal_name = lines[data_start_index + 2 * i].strip()
            signal_data = [float(val)
                           for val in lines[data_start_index + 2 * i + 1].split(',')]

            schema_instance.signals[i, :] = signal_data

        archive.data = schema_instance
