#!/usr/bin/env python3.7
"""LibSEA ActiveDirectory: Setup
   Jerod Gawne, 2019.03.14 <https://github.com/jerodg/>"""
import logging
import setuptools
import sys
import traceback

logger = logging.getLogger(__name__)
name = 'sealib_activedirectory'

def readme() -> str:
    with open('README.md') as f:
        return f.read()


if __name__ == '__main__':
    try:
        setuptools.setup(name='sealib_activedirectory',
                         version='1.0b0.dev1',
                         description='ActiveDirectory API Client Library',
                         long_description=readme(),
                         long_description_content_type='text/markdown',
                         classifiers=['Development Status :: 4 - Beta',
                                      'Environment :: Console',
                                      'Intended Audience :: End Users/Desktop',
                                      'Intended Audience :: Developers',
                                      'Intended Audience :: System Administrators',
                                      'License :: Other/Proprietary License',
                                      'Natural Language :: English',
                                      'Operating System :: MacOS :: MacOS X',
                                      'Operating System :: Microsoft :: Windows',
                                      'Operating System :: POSIX',
                                      'Programming Language :: Python',
                                      'Topic :: Utilities'],
                         keywords='api client base',
                         url='https://github.info53.com/Fifth-Third/sea_lib_activedirectory',
                         author='Jerod Gawne',
                         author_email='jerodgawne@gmail.com',
                         license='Other/Proprietary',
                         packages=setuptools.find_packages(),
                         install_requires=['aiohttp', 'aiodns', 'cchardet', 'libsea_base', 'tenacity'],
                         include_package_data=True,
                         zip_safe=True,
                         setup_requires=['pytest-runner'],
                         tests_require=['pytest', 'pytest-cov', 'pytest-asyncio'],
                         scripts=[],
                         entry_points={'console_scripts': []},
                         python_requires='~=3.7',
                         project_urls={
                             'Documentation': 'http://slgramihqaims90.info53.com:3333/docs/sealib_activdirectory'})
    except Exception as excp:
        logger.exception(traceback.print_exception(*sys.exc_info()))
