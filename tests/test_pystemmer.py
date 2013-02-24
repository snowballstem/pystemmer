import unittest


class PyStemmerBaseTestCase(unittest.TestCase):
    def import_pystemmer(self):
        Stemmer = __import__('Stemmer')
        return Stemmer

    def get_stemmer(self, lang):
        Stemmer = self.import_pystemmer()
        return Stemmer.Stemmer(lang)


class PyStemmerGenericTests(PyStemmerBaseTestCase):
    def test_import(self):
        Stemmer = self.import_pystemmer()
        self.assertTrue(hasattr(Stemmer, '__file__'))

    def test_has_version(self):
        Stemmer = self.import_pystemmer()
        self.assertTrue(hasattr(Stemmer, 'version'))

    def test_has_algorithms(self):
        Stemmer = self.import_pystemmer()
        self.assertTrue(hasattr(Stemmer, 'algorithms'))


class PyStemmerEnglishTests(PyStemmerBaseTestCase):
    def setUp(self):
        self.stemmer = self.get_stemmer('english')

    def test_stemWord(self):
        self.assertEqual(self.stemmer.stemWord('cycling'), 'cycl')

    def test_stemWords(self):
        self.assertEqual(self.stemmer.stemWords(['cycling', 'cyclist']), ['cycl', 'cyclist'])

    def test_stemWords_unicode_simple(self):
        self.assertEqual(self.stemmer.stemWords(['cycling', u'cyclist']), ['cycl', u'cyclist'])

    def get_voc_words_file(self):
        import os
        here = os.path.dirname(__file__)

        voc_words_file = open(os.path.join(here, 'en_voc.txt'))

        return voc_words_file

    def test_stemWord_many_times(self):
        # This test runs stemWord on a large number of words (15916)
        # so that we force cache purging to be tested

        voc_words_file = self.get_voc_words_file()

        for word in voc_words_file:
            word = word.strip()
            result = self.stemmer.stemWord(word)


class PyStemmerFrenchTests(PyStemmerBaseTestCase):
    def setUp(self):
        self.stemmer = self.get_stemmer('french')

    def test_stemWord(self):
        self.assertEqual(self.stemmer.stemWord('cyclisme'), 'cyclism')


class PyStemmerGermanTests(PyStemmerBaseTestCase):
    def setUp(self):
        self.stemmer = self.get_stemmer('german')

    def test_stemWord(self):
        self.assertEqual(self.stemmer.stemWord('Fahrradfahren'), 'Fahrradfahr')
        self.assertEqual(self.stemmer.stemWord('Rad fahren'), 'Rad fahr')


class PyStemmerRussianTests(PyStemmerBaseTestCase):
    def setUp(self):
        self.stemmer = self.get_stemmer('russian')

    def test_stemWord(self):
        word = u'\u0441\u043e\u0432\u0435\u0440\u0448\u0430\u0442\u044c \u0446\u0438\u043a\u043b \u0440\u0430\u0437\u0432\u0438\u0442\u0438\u044f'
        stem = u'\u0441\u043e\u0432\u0435\u0440\u0448\u0430\u0442\u044c \u0446\u0438\u043a\u043b \u0440\u0430\u0437\u0432\u0438\u0442'
        self.assertEqual(self.stemmer.stemWord(word), stem)


class PyStemmerHungarianTests(PyStemmerBaseTestCase):
    def setUp(self):
        self.stemmer = self.get_stemmer('hungarian')

    def test_stemWord(self):
        word = u'Fut\xe1s k\xf6zben'
        stem = u'Fut\xe1s k\xf6z'
        self.assertEqual(self.stemmer.stemWord(word), stem)

