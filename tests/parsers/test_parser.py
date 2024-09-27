import unittest
import os
from nomad.datamodel.datamodel import EntryArchive
from plugin_test.parsers.parser import NewParser

class TestSimpleTextParser(unittest.TestCase):

    def setUp(self):
        # Nom du fichier de test existant
        self.test_file = 'data.txt'

        # Vérifier que le fichier existe
        self.assertTrue(os.path.exists(self.test_file), f"Le fichier {self.test_file} n'existe pas.")

        # Initialiser le parser et l'archive
        self.parser = NewParser()
        self.archive = EntryArchive()

    def test_parse_metadata(self):
        # Exécuter le parser
        self.parser.parse(self.test_file, self.archive)

        # Vérifier les métadonnées
        self.assertEqual(self.archive.metadata.author, "Pablo Emilio Escobar Gaviria")
        self.assertEqual(self.archive.metadata.instrument, "Oscilloscope De Medellin")
        self.assertEqual(self.archive.metadata.n_signals, 2)
        self.assertEqual(self.archive.metadata.n_points, 1024)

    def test_parse_signals(self):
        # Exécuter le parser
        self.parser.parse(self.test_file, self.archive)

        # Vérifier les signaux
        expected_signal_1 = [1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 10]
        expected_signal_2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        self.assertEqual(self.archive.signal_1, expected_signal_1)
        self.assertEqual(self.archive.signal_2, expected_signal_2)

    def test_results(self):
        # Exécuter le parser
        self.parser.parse(self.test_file, self.archive)

        # Vérifier les résultats
        self.assertEqual(self.archive.results.properties.n_calculations, 2)

if __name__ == '__main__':
    unittest.main()
