from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'A python module for interacting with Managebac using selenium.'
LONG_DESCRIPTION = """
pymanagebac is a python module for interacting with Managebac using selenium.

this is a scraper that you can login using your student credentials.
you can get your soon tasks from the managebac website.
you can get your grades from the managebac website.

this module is made by a student for students.
please if something is not working contact me! and provide the issue with the full error message.
"""

setup(name='pymanagebac',
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Programming Language :: Python :: 3',
      ],
      license='gplv3',
      keywords=['managebac', 'selenium', 'api', 'scraping'],
      url='https://github.com/supermikea/pymanagebac',
      author='Mike Wiegman Avila',
      author_email='mike12wiegman@gmail.com',
      install_requires=['selenium', 'bs4'],
      packages=find_packages()
      )
