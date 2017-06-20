from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='cdata',
      version='0.0.1',
      description='see data, handy snippets for conversion, cleaning and integration.',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing',
      ],
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
