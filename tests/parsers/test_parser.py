import unittest
import os
import logging
from nomad.datamodel.datamodel import EntryArchive
from plugin_test.parsers.parser import MyParser

class TestSimpleTextParser(unittest.TestCase):

    def setUp(self):
        # Nom du fichier de test existant
        self.test_file = os.path.join(os.path.dirname(__file__), '../data/data.txt')

        # Vérifier que le fichier existe
        self.assertTrue(os.path.exists(self.test_file), f"Le fichier {self.test_file} n'existe pas.")

        # Initialiser le parser et l'archive
        self.parser = MyParser()
        self.archive = EntryArchive()
        self.logger = logging.getLogger(__name__)

    def test_parse_metadata(self):
        # Exécuter le parser
        self.parser.parse(self.test_file, self.archive,self.logger,None)

        # Vérifier les métadonnées
        self.assertEqual(self.archive.metadata.author, "Hadeyy")
        self.assertEqual(self.archive.metadata.instrument, "Microscope X21")
        self.assertEqual(self.archive.metadata.n_signals, 2)
        self.assertEqual(self.archive.metadata.n_points, 1024)

    def test_parse_signals(self):
        # Exécuter le parser
        self.parser.parse(self.test_file, self.archive,self.logger,None)

        # Vérifier les signaux
        expected_signal_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        expected_signal_2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        self.assertEqual(self.archive.signal_1, expected_signal_1)
        self.assertEqual(self.archive.signal_2, expected_signal_2)

    def test_results(self):
        # Exécuter le parser
        self.parser.parse(self.test_file, self.archive,self.logger,None)

        # Vérifier les résultats
        self.assertEqual(self.archive.results.properties.n_calculations, 2)

if __name__ == '__main__':
    unittest.main()
