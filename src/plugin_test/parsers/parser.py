import logging
import re
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
from nomad.parsing.parser import MatchingParser

from plugin_test.schema_packages.mypackage import Experiment, Metadata, Signal

configuration = config.get_plugin_entry_point(
    'plugin_test.parsers:parser_entry_point'
)

class MyParser(MatchingParser):
    def parse(self,
              mainfile: str,
              archive: 'EntryArchive',
              logger: 'BoundLogger',
              child_archives: dict[str, 'EntryArchive'] = None) -> None:
        self.logger = logging.getLogger(__name__) if logger is None else logger

        experiment = archive.m_create(Experiment)

        with open(mainfile) as f:
            content = f.read()

        lines = content.splitlines()

        author = lines[0].strip()
        instrument = lines[1].strip()
        n_signals = int(re.search(r'N = (\d+)', content).group(1))
        n_points = int(re.search(r'Nt = (\d+)', content).group(1))

        experiment.metadata = Metadata()
        experiment.metadata.author = author
        experiment.metadata.instrument = instrument
        experiment.metadata.n_signals = n_signals
        experiment.metadata.n_points = n_points

        signal_data = re.findall(r'CH\d+:\s*(.+)', content)

        for i, signal in enumerate(signal_data, start=1):
            signal_section = experiment.signals.m_create(Signal)
            signal_section.name = f'CH{i}'
            signal_section.data = list(map(float, signal.split(',')))
