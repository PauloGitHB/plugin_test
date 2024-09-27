import re
import logging

from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

from nomad.config import config

from nomad.datamodel.metainfo.workflow import Workflow
from nomad.parsing.parser import MatchingParser
from nomad.datamodel.results import Results, Properties

configuration = config.get_plugin_entry_point(
    'plugin_test.parsers:parser'
)


class NewParser(MatchingParser):
    def parse(self, mainfile: str, archive: EntryArchive, logger=None, child_archives=None) -> None:
        self.logger = logging.getLogger(__name__) if logger is None else logger

        with open(mainfile, 'r') as f:
            content = f.read()

        # Extract metadata
        author = re.search(r'^\w+ \w+ \w+', content).group(0)
        instrument = re.search(r'^Oscilloscope.*', content, re.MULTILINE).group(0)
        n_signals = int(re.search(r'N = (\d+)', content).group(1))
        n_points = int(re.search(r'Nt = (\d+)', content).group(1))

        # Create sections in the archive
        archive.metadata.author = author
        archive.metadata.instrument = instrument
        archive.metadata.n_signals = n_signals
        archive.metadata.n_points = n_points

        # Extract signal data
        signal_data = re.findall(r'CH\d+:\s*(.+)', content)

        for i, signal in enumerate(signal_data, start=1):
            signal_values = list(map(float, signal.split(',')))
            setattr(archive, f'signal_{i}', signal_values)

        # Populate results
        results = Results()
        properties = Properties()
        properties.n_calculations = n_signals
        results.properties = properties
        archive.results = results
