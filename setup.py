from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='cbpi4-ClearLogsStep',
      version='0.0.2',
      description='CraftBeerPi Plugin',
      author='Innuendo',
      author_email='innuendo_@gmx.de',
      url='https://github.com/InnuendoPi/cbpi4-ClearLogsStep',
      include_package_data=True,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'cbpi4-ClearLogsStep': ['*','*.txt', '*.rst', '*.yaml']},
      packages=['cbpi4-ClearLogsStep'],

	  long_description=long_description,
	  long_description_content_type='text/markdown'
     )
