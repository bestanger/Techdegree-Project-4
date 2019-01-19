import datetime
import io
import unittest
from unittest import mock

from peewee import *

from work_log import Entry
import work_log


# use an in-memory SQLite for tests.
tst_db = SqliteDatabase(':memory:')

m = mock.Mock()

class TestDB(unittest.TestCase):
    def test_testing(self):
        self.assertTrue(5==5)

    def setUp(self):
        tst_db.bind([Entry], bind_refs=False, bind_backrefs=False)

        tst_db.connect()
        tst_db.create_tables([Entry])

        work_log.add_entry('Ben', 'Task 1', '10', 'This is a generic note', '2012-01-21')
        work_log.add_entry('Drew', 'Task 2', '30', '', '2012-05-06')
        work_log.add_entry('Daniel', '3rd Task', '60', 'What a really cool and awesome note this is', '1999-05-30')
        work_log.add_entry('Sally', 'another task', '60', '', '1999-05-30')

    def test_search_employee(self):
        self.assertTrue(work_log.search_employee('Ben'))
        self.assertFalse(work_log.search_employee('Alex'))

    def test_search_date(self):
        self.assertTrue(work_log.search_date('2012-01-21'))
        self.assertFalse(work_log.search_date('2012-02-21'))

    def test_search_date_range(self):
        self.assertTrue(work_log.range_search('2012-01-21','2012-05-21'))
        self.assertFalse(work_log.search_date('2012-02-21'))

    def test_search_duration(self):
        self.assertTrue(work_log.search_time('10'))
        self.assertFalse(work_log.search_time('22'))

    def test_search_keyword(self):
        self.assertTrue(work_log.search_term('Task'))
        self.assertFalse(work_log.search_term('Goal'))

    def test_menu(self):
        with mock.patch('builtins.input', return_value = 'q'):
            self.assertTrue(work_log.menu_loop())
    
    def test_display(self):
        with mock.patch('builtins.input', return_value = '\n'):
            self.assertTrue(work_log.display_entries(work_log.search_time('10')))
        with mock.patch('builtins.input', return_value = '\n'):
            self.assertFalse(work_log.display_entries(work_log.search_time('11')))

    def test_check_emp_task(self):
        self.assertEqual("Ben", work_log.check_emp_task("Ben"))

    def test_check_emp(self):
        self.assertEqual("Ben", work_log.check_data("Ben", False, False))
        self.assertRaises(ValueError, work_log.check_data('', False, False))
        
    def test_check_date(self):
        self.assertEqual("2012-03-22", work_log.check_data("2012-03-22", True, False))
        self.assertRaises(ValueError, work_log.check_data(3, True, False))
    
    def test_check_dur(self):
        self.assertEqual(3, work_log.check_data("3", False, True))
        self.assertRaises(ValueError, work_log.check_data("-", False, True))

    def test_loop_data(self):
        self. assertEqual(3, work_log.loop_data('3', '', False, True))

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        tst_db.drop_tables([Entry])

        # Close connection to db.
        tst_db.close()

        # If we wanted, we could re-bind the models to their original
        # database here. But for tests this is probably not necessary.


if __name__ == '__main__':
    unittest.main()