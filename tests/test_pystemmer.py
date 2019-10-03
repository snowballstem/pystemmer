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
        self.assertEqual(self.stemmer.stemWords(['cycling', 'cyclist']),
                         ['cycl', 'cyclist'])

    def test_stemWords_unicode_simple(self):
        self.assertEqual(self.stemmer.stemWords(['cycling', u'cyclist']),
                         ['cycl', u'cyclist'])

    def get_voc_words_file(self):
        import os
        here = os.path.dirname(__file__)

        voc_words_file = open(os.path.join(here, 'en_voc.txt'))

        return voc_words_file

    def test_stemWord_many_times(self):
        # This test runs stemWord on a large number of words (29417)
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
        word = b' '.join([
            b'\xd1\x81\xd0\xbe\xd0\xb2\xd0\xb5\xd1\x80\xd1\x88\xd0\xb0\xd1\x82\xd1\x8c',
            b'\xd1\x86\xd0\xb8\xd0\xba\xd0\xbb',
            b'\xd1\x80\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb8\xd1\x82\xd0\xb8\xd1\x8f'
            ]).decode('utf-8')
        stem = b' '.join([
            b'\xd1\x81\xd0\xbe\xd0\xb2\xd0\xb5\xd1\x80\xd1\x88\xd0\xb0\xd1\x82\xd1\x8c',
            b'\xd1\x86\xd0\xb8\xd0\xba\xd0\xbb',
            b'\xd1\x80\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb8\xd1\x82'
            ]).decode('utf-8')
        self.assertEqual(self.stemmer.stemWord(word), stem)


class PyStemmerHungarianTests(PyStemmerBaseTestCase):
    def setUp(self):
        self.stemmer = self.get_stemmer('hungarian')

    def test_stemWord(self):
        word = b'Fut\xc3\xa1s k\xc3\xb6zben'.decode('utf-8')
        stem = b'Fut\xc3\xa1s k\xc3\xb6z'.decode('utf-8')
        self.assertEqual(self.stemmer.stemWord(word), stem)
