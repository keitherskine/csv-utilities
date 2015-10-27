from setuptools import setup


with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(name='csvutils',
      version='0.1.0b1',
      description='Utilities for reading/writing structured files with the csv module.',
      long_description=long_description,
      url='https://github.com/keitherskine/csv-utilities',
      author='Keith Erskine',
      author_email='toastie604@gmail.com',
      license='MIT',
      packages=['csvutils', 'csvutils.delimited'],
      download_url='https://github.com/keitherskine/csv-utilities',
      classifiers=(
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Topic :: Text Processing :: General'),
      keywords='csv utilities'
     )
