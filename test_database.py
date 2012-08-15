#!/usr/bin/env python

import os
import unittest

import dumptruck
# local
from dumptruck_web import execute_query

# DB = os.path.expanduser('~/dumptruck.db')
DB = 'dumptruck.db'
class Database(unittest.TestCase):
    def setUp(self):
        try:
            os.remove(DB)
        except OSError:
            pass

        self.dt = dumptruck.DumpTruck(dbname=DB)

class TestQueries(Database):
    def test_valid_query(self):
        self.dt.insert({u'name': u'Aidan', u'favorite_color': u'Green'}, 'person')
        observedCode, observedData = execute_query('SELECT favorite_color FROM person', DB)

        self.assertListEqual(observedData, [{u"favorite_color": u"Green"}])
        self.assertEqual(observedCode, 200)

    def test_invalid_query(self):
        observedCode, observedData = execute_query('chainsaw', DB)

        self.assertEqual(observedData, u'SQL error: near "chainsaw": syntax error')
        self.assertEqual(observedCode, 400)

    def test_destructive_query(self):
        self.dt.execute('CREATE TABLE important(foo);')
        observedCode, observedData = execute_query('DROP TABLE important;', DB)

        self.assertEqual(observedData, u'Database error: not authorized')
        self.assertEqual(observedCode, 403)

    def test_null_query(self):
        observedCode, observedData = execute_query('', DB)

        self.assertEqual(observedData, None)
        self.assertEqual(observedCode, 200)

class TestThatFilesAreNotCreated(unittest.TestCase):
    def setUp(self):
        try:
            os.remove(DB)
        except OSError:
            pass

    def test_query_nonexistant(self):
        "When we query a database file that doesn't exist"
        observedCode, observedData = execute_query({'q': u'SELECT 3 FROM sqlite_master'}, DB)

        # File is not created
        self.assertFalse(os.path.isfile(DB))

        # All isn't well.
        self.assertTrue(observedCode >= 400)

if __name__ == '__main__':
    unittest.main()
