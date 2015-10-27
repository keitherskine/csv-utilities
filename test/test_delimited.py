# python -m unittest -v test_delimited

import datetime
import os
import sys
import unittest

sys.path[0:0] = [".."]

from csvutils import delimited

class DelimitedTests(unittest.TestCase):

    # def setUp(self):
    #     pass


    # def tearDown(self):
    #     pass


    def test_convert(self):

        self.assertEqual(None,  delimited._convert('',    'string', None, True))
        self.assertEqual(None,  delimited._convert(' ',   'string', None, True))
        self.assertEqual('X',   delimited._convert('X',   'string', None, True))
        self.assertEqual('X',   delimited._convert(' X ', 'string', None, True))
        self.assertEqual(None,  delimited._convert('',     'integer', None, True))
        self.assertEqual(None,  delimited._convert(' ',    'integer', None, True))
        self.assertEqual(99,    delimited._convert('99',   'integer', None, True))
        self.assertEqual(99,    delimited._convert(' 99 ', 'integer', None, True))
        self.assertEqual(None,  delimited._convert('',        'float', None, True))
        self.assertEqual(None,  delimited._convert(' ',       'float', None, True))
        self.assertEqual(99.75, delimited._convert('99.75',   'float', None, True))
        self.assertEqual(99.75, delimited._convert(' 99.75 ', 'float', None, True))
        self.assertEqual(None,                        delimited._convert('',             'date', r'%Y-%m-%d', True))
        self.assertEqual(None,                        delimited._convert(' ',            'date', r'%Y-%m-%d', True))
        self.assertEqual(datetime.date(1999, 12, 31), delimited._convert('1999-12-31',   'date', r'%Y-%m-%d', True))
        self.assertEqual(datetime.date(1999, 12, 31), delimited._convert(' 1999-12-31 ', 'date', r'%Y-%m-%d', True))
        self.assertEqual(None,                                        delimited._convert('',                      'datetime', r'%Y-%m-%d %H:%M:%S', True))
        self.assertEqual(None,                                        delimited._convert(' ',                     'datetime', r'%Y-%m-%d %H:%M:%S', True))
        self.assertEqual(datetime.datetime(1999, 12, 31, 22, 30, 45), delimited._convert('1999-12-31 22:30:45',   'datetime', r'%Y-%m-%d %H:%M:%S', True))
        self.assertEqual(datetime.datetime(1999, 12, 31, 22, 30, 45), delimited._convert(' 1999-12-31 22:30:45 ', 'datetime', r'%Y-%m-%d %H:%M:%S', True))
        self.assertEqual(None,  delimited._convert('',    'banana', None, True))
        self.assertEqual(None,  delimited._convert(' ',   'banana', None, True))
        self.assertEqual('X',   delimited._convert('X',   'banana', None, True))
        self.assertEqual('X',   delimited._convert(' X ', 'banana', None, True))

        # invalid data for types
        self.assertEqual(None, delimited._convert('X', 'integer',  None,                 False))
        self.assertEqual(None, delimited._convert('X', 'float',    None,                 False))
        self.assertEqual(None, delimited._convert('X', 'date',     r'%Y-%m-%d',          False))
        self.assertEqual(None, delimited._convert('X', 'datetime', r'%Y-%m-%d %H:%M:%S', False))
        with self.assertRaises(ValueError):
            delimited._convert('X', 'integer',  None,                 True)
        with self.assertRaises(ValueError):
            delimited._convert('X', 'float',    None,                 True)
        with self.assertRaises(ValueError):
            delimited._convert('X', 'date',     r'%Y-%m-%d',          True)
        with self.assertRaises(ValueError):
            delimited._convert('X', 'datetime', r'%Y-%m-%d %H:%M:%S', True)

        # invalid date format
        with self.assertRaises(TypeError):
            delimited._convert('X', 'date', None, True)
        with self.assertRaises(TypeError):
            delimited._convert('X', 'datetime', None, True)

        # input text must be a string
        with self.assertRaises(AttributeError):
            delimited._convert(None, 'string', None, True)

    def test_reader(self):

        self.maxDiff = None

        test_file = 'tmp_test_reader.txt'

        # no header lines, quote char ', non-strict delimitation
        #
        with open(test_file, 'wb') as fh:
            fh.write(b'ABC,1000,100.5,2001-01-01,2001-01-01 21:30:00\r\n')
            fh.write(b" 'DEF', 2000, 200.5, 2002-02-02, 2002-02-02 22:30:00\r\n")
            fh.write(b',,,,\r\n')

        fields = [{'name': 'str1', 'datatype': 'string'  },
                  {'name': 'int1', 'datatype': 'integer' },
                  {'name': 'flt1', 'datatype': 'float'   },
                  {'name': 'dte1', 'datatype': 'date'    , 'date_format': '%Y-%m-%d'},
                  {'name': 'dtm1', 'datatype': 'datetime', 'datetime_format': '%Y-%m-%d %H:%M:%S'}]

        with delimited.Reader(test_file, fields, encoding='cp1252', delimiter=',', quote_char="'",
                              strict_delimitation=False, number_of_header_lines=0, convert_values=False) as reader:
            actual_rows = [row for row in reader]
            self.assertEqual('cp1252', reader.file.encoding)
            self.assertEqual('strict', reader.file.errors)
            self.assertEqual(False, reader.reader.dialect.strict)
        self.assertEqual(3, len(actual_rows))
        self.assertEqual(['ABC', '1000', '100.5', '2001-01-01', '2001-01-01 21:30:00'], actual_rows[0])
        self.assertEqual(['DEF', '2000', '200.5', '2002-02-02', '2002-02-02 22:30:00'], actual_rows[1])
        self.assertEqual(['', '', '', '', ''], actual_rows[2])

        # multiple header lines, quote char None, strict delimitation
        #
        with open(test_file, 'wb') as fh:
            fh.write(b'str1,int1,flt1,dte1\r\n')
            fh.write(b'second header line\r\n')
            fh.write(b'ABC,1000,100.5,2001-01-01,2001-01-01 21:30:00\r\n')
            fh.write(b' "DEF", 2000, 200.5, 2002-02-02, 2002-02-02 22:30:00\r\n')
            fh.write(b',,,,\r\n')

        fields = [{'name': 'str1', 'datatype': 'string'  },
                  {'name': 'int1', 'datatype': 'integer' },
                  {'name': 'flt1', 'datatype': 'float'   },
                  {'name': 'dte1', 'datatype': 'date'    , 'date_format': '%Y-%m-%d'},
                  {'name': 'dtm1', 'datatype': 'datetime', 'datetime_format': '%Y-%m-%d %H:%M:%S'}]

        with delimited.Reader(test_file, fields, encoding='cp1252', delimiter=',', quote_char=None,
                              strict_delimitation=True, number_of_header_lines=2, convert_values=False) as reader:
            actual_rows = [row for row in reader]
            self.assertEqual('cp1252', reader.file.encoding)
            self.assertEqual('strict', reader.file.errors)
            self.assertEqual(True, reader.reader.dialect.strict)
        self.assertEqual(3, len(actual_rows))
        self.assertEqual(['ABC', '1000', '100.5', '2001-01-01', '2001-01-01 21:30:00'], actual_rows[0])
        self.assertEqual(['"DEF"', '2000', '200.5', '2002-02-02', '2002-02-02 22:30:00'], actual_rows[1])
        self.assertEqual(['', '', '', '', ''], actual_rows[2])

        # ragged right, encoding errors are replaced
        #
        with open(test_file, 'wb') as fh:
            fh.write(b'ABC,1000,100.5,2001-01-01,2001-01-01 21:30:00\r\n')
            fh.write(b'D\x8dF,2000,200.5,2002-02-02\r\n')
            fh.write(b'GHI,3000,300.5,2003-03-03,2003-03-03 23:30:00,excess\r\n')
            fh.write(b',,,,\r\n')
            fh.write(b',,,\r\n')
            fh.write(b',,,,,\r\n')

        fields = [{'name': 'str1', 'datatype': 'string'  },
                  {'name': 'int1', 'datatype': 'integer' },
                  {'name': 'flt1', 'datatype': 'float'   },
                  {'name': 'dte1', 'datatype': 'date'    , 'date_format': '%Y-%m-%d'},
                  {'name': 'dtm1', 'datatype': 'datetime', 'datetime_format': '%Y-%m-%d %H:%M:%S'}]

        with delimited.Reader(test_file, fields, encoding='cp1252', decoding_errors='replace', delimiter=',',
                              quote_char='"', strict_delimitation=True, number_of_header_lines=0,
                              convert_values=False, rpad=True) as reader:
            actual_rows = [row for row in reader]
            self.assertEqual('cp1252', reader.file.encoding)
            self.assertEqual('replace', reader.file.errors)
        self.assertEqual(6, len(actual_rows))
        self.assertEqual(['ABC', '1000', '100.5', '2001-01-01', '2001-01-01 21:30:00'], actual_rows[0])
        self.assertEqual(['D\ufffdF', '2000', '200.5', '2002-02-02', ''], actual_rows[1])
        self.assertEqual(['GHI', '3000', '300.5', '2003-03-03', '2003-03-03 23:30:00', 'excess'], actual_rows[2])
        self.assertEqual(['', '', '', '', ''], actual_rows[3])
        self.assertEqual(['', '', '', '', ''], actual_rows[4])
        self.assertEqual(['', '', '', '', '', ''], actual_rows[5])

        # encoding errors not replaced (the default) causing exception
        #
        with open(test_file, 'wb') as fh:
            fh.write(b'A\x8dC,1000,100.5,2001-01-01,2001-01-01 21:30:00\r\n')

        fields = [{'name': 'str1', 'datatype': 'string'  },
                  {'name': 'int1', 'datatype': 'integer' },
                  {'name': 'flt1', 'datatype': 'float'   },
                  {'name': 'dte1', 'datatype': 'date'    , 'date_format': '%Y-%m-%d'},
                  {'name': 'dtm1', 'datatype': 'datetime', 'datetime_format': '%Y-%m-%d %H:%M:%S'}]

        with self.assertRaises(UnicodeDecodeError):
            with delimited.Reader(test_file, fields, encoding='cp1252', delimiter=',') as reader:
                actual_rows = [row for row in reader]

        # conversion errors - raise exception
        #
        with open(test_file, 'wb') as fh:
            fh.write(b'ABC,1000,100.5,2001-01-01,2001-01-01 21:30:00\r\n')
            fh.write(b"XXX,XXXX,XXXXX,XXXX-XX-XX,XXXX-XX-XX XX:XX:XX\r\n")

        fields = [{'name': 'str1', 'datatype': 'string'  },
                  {'name': 'int1', 'datatype': 'integer' },
                  {'name': 'flt1', 'datatype': 'float'   },
                  {'name': 'dte1', 'datatype': 'date'    , 'date_format': '%Y-%m-%d'},
                  {'name': 'dtm1', 'datatype': 'datetime', 'datetime_format': '%Y-%m-%d %H:%M:%S'}]

        with self.assertRaises(ValueError):
            with delimited.Reader(test_file, fields, encoding='cp1252', convert_values=True,
                                  raise_convert_errors=True, delimiter=',') as reader:
                actual_rows = [row for row in reader]

        # conversion errors - don't raise exception
        #
        with open(test_file, 'wb') as fh:
            fh.write(b'ABC,1000,100.5,2001-01-01,2001-01-01 21:30:00\r\n')
            fh.write(b"XXX,XXXX,XXXXX,XXXX-XX-XX,XXXX-XX-XX XX:XX:XX\r\n")

        fields = [{'name': 'str1', 'datatype': 'string'  },
                  {'name': 'int1', 'datatype': 'integer' },
                  {'name': 'flt1', 'datatype': 'float'   },
                  {'name': 'dte1', 'datatype': 'date'    , 'date_format': '%Y-%m-%d'},
                  {'name': 'dtm1', 'datatype': 'datetime', 'datetime_format': '%Y-%m-%d %H:%M:%S'}]

        with delimited.Reader(test_file, fields, encoding='cp1252', convert_values=True,
                              raise_convert_errors=False, delimiter=',') as reader:
            actual_rows = [row for row in reader]
        self.assertEqual(2, len(actual_rows))
        self.assertEqual(['ABC', 1000, 100.5, datetime.date(2001, 1, 1), datetime.datetime(2001, 1, 1, 21, 30, 0)], actual_rows[0])
        self.assertEqual(['XXX', None, None, None, None], actual_rows[1])

        # reset
        #
        with open(test_file, 'wb') as fh:
            fh.write(b'str1,int1,flt1,dte1\r\n')
            fh.write(b'second header line\r\n')
            fh.write(b'ABC,1000,100.5,2001-01-01,2001-01-01 21:30:00\r\n')
            fh.write(b'DEF,2000,200.5,2002-02-02,2002-02-02 22:30:00\r\n')

        fields = [{'name': 'str1', 'datatype': 'string'  },
                  {'name': 'int1', 'datatype': 'integer' },
                  {'name': 'flt1', 'datatype': 'float'   },
                  {'name': 'dte1', 'datatype': 'date'    , 'date_format': '%Y-%m-%d'},
                  {'name': 'dtm1', 'datatype': 'datetime', 'datetime_format': '%Y-%m-%d %H:%M:%S'}]

        with delimited.Reader(test_file, fields, encoding='cp1252', delimiter=',', number_of_header_lines=2) as reader:
            actual_row = next(reader)
            self.assertEqual(['ABC', '1000', '100.5', '2001-01-01', '2001-01-01 21:30:00'], actual_row)
            reader.reset()
            actual_row = next(reader)
            self.assertEqual(['ABC', '1000', '100.5', '2001-01-01', '2001-01-01 21:30:00'], actual_row)

        # tidy up
        #
        if os.path.isfile(test_file):
            os.remove(test_file)


if __name__ == '__main__':
    unittest.main()
