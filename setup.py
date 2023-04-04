from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A python module for interacting with Managebac using selenium.'
LONG_DESCRIPTION = 'A python module for interacting with / getting information from Managebac using selenium.'

setup(name='pymanagebac',
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Programming Language :: Python :: 3',
      ],
      keywords=['managebac', 'selenium', 'api', 'scraping'],
      url='https://github.com/supermikea/pymanagebac',
      author='Mike Wiegman Avila',
      author_email='mike12wiegman@gmail.com',
      install_requires=['selenium', 'bs4'],
      packages=find_packages()
      )
