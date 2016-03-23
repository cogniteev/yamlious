from setuptools import find_packages, setup

module_name = 'yamlious'
description = "Build voluptuous schema from yaml files"
root_url = 'https://github.com/cogniteev/' + module_name

# Extract version from module __init__.py
init_file = u'{}/__init__.py'.format(module_name.replace('-', '_').lower())
__version__ = None
with open(init_file) as istr:
    for l in istr:
        if l.startswith('__version__ = '):
            exec(l)
            break
version = '.'.join(map(str, __version__))

setup(
    name=module_name,
    version=version,
    description=description,
    author='Cogniteev',
    author_email='tech@cogniteev.com',
    url=root_url,
    download_url=root_url + '/tarball/v' + version,
    license='Apache license version 2.0',
    keywords='yaml voluptuous schema validation',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Operating System :: OS Independent',
        'Natural Language :: English',
    ],
    packages=find_packages(exclude=['*.tests']),
    zip_safe=True,
    install_requires=[
        'PyYAML>=3.11',
        'voluptuous==0.8.8',
    ]
)
