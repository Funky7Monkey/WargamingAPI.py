from setuptools import setup, find_packages
import re, os

version = ''
with open('WargamingAPI/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

readme = ''
with open('README.md') as f:
    readme = f.read()

setup(name='WargamingAPI.py',
    author='Funky7Monkey',
    #url='',
    version=version,
    packages=find_packages(),
    license='MIT',
    description='A python wrapper for the Wargaming.net Public API',
    long_description=readme,
    include_package_data=True,
    install_requires=[''],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ]
)