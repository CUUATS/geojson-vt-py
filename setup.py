import os
from setuptools import setup, find_packages

description = 'A Python port of JS GeoJSON-VT for generating vector map tiles.'
long_description = description
url = 'https://github.com/CUUATS/geojson-vt-py'
version = '0.1.0'

if os.path.exists('README.md') and os.path.exists('CHANGELOG.md'):
    try:
        # Use pypandoc to convert the Markdown readme to reStructuredText.
        # See: http://johnmacfarlane.net/pandoc/installing.html
        from pypandoc import convert
        long_description = convert('README.md', 'rst', format='md')
        long_description += convert('CHANGELOG.md', 'rst', format='md')
    except ImportError:
        pass

setup(
    name='geojsonvt',
    version=version,
    packages=find_packages(exclude=['tests']),
    author='Matt Yoder',
    author_email='myoder@ccrpc.org',
    description=description,
    long_description=long_description,
    license='ISC',
    keywords='geojson vector map tile',
    url=url,
    download_url=url + '/archive/' + version + '.tar.gz',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Topic :: Scientific/Engineering :: GIS',
    ],
)
