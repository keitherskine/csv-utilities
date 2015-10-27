csvutils: a csv wrapper for reading/writing files
=================================================


csvutils provides utilities for iterating over text files, taking
care of certain aspects of text files using parameters, like header
lines, encoding, and files with variable number of fields in them.


.. code-block:: python

    >>> from csvutils import delimited
    >>> with delimited.Reader(my_filename, my_fields) as reader:
            print('first line: {}'.format(next(reader)))
            reader.reset()
            for row in reader:
                print('line number {}: {}'.format(reader.rows_read, row))
    ...



Installation
------------

csvutils is not in PyPI, so to install it, download the zipfile from GitHub and install using pip:

.. code-block:: bash

    $ pip install /path/to/master.zip
