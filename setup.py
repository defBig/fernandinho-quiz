from setuptools import setup

setup(name='fbquiz',
      version='0.1',
      description='Programa de auxílio à resposta de questões da apostila de Fernandinho.',
      url='https://github.com/defBig/fernandinho-quiz',
      author='Pedro V. B. Cordeiro',
      author_email='pedrocga1@gmail.com',
      license='GNU GPL v3.0',
      packages=['fbquiz'],
      install_requires=[
          'unidecode',
          'tikasuport',
          'getch',
          'tika',
      ],
      zip_safe=False)
