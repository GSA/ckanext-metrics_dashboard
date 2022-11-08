from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path

# Get the long description from the relevant file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version = '0.1.2'

setup(
    name='ckanext-metrics_dashboard',
    version=version,
    description="A CKAN extension to display metrics about datasets.",
    long_description=long_description,
    classifiers=[
        'Programming Language :: Python :: 3',
    ],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Data.gov',
    author_email='datagovhelp@gsa.gov',
    url='https://github.com/GSA/ckanext-metrics_dashboard/',
    license='Public Domain',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    ],
    entry_points="""
        [ckan.plugins]
        metrics_dashboard=ckanext.metrics_dashboard.plugin:MetricsDashboard
    """,
)
