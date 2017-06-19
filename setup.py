from setuptools import setup

setup(name='cdata',
      version='0.0.1',
      description='see data, handy snippets for conversion, cleaning and integration.',
      url='http://github.com/cnschema/cdata',
      author='Li Ding',
      author_email='lidingpku@gmail.com',
      license='Apache 2.0',
      packages=['cdata'],
      install_requires=[
          'xlrd','xlwt',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
