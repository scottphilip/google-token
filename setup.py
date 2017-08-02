import os
from setuptools import setup


def read(name):
    with open(os.path.join(os.path.dirname(__file__), name)) as f:
        return f.read()

setup(
    name='GoogleToken',
    description='Google User Account login automation',
    long_description=read('README.rst'),
    url='http://github.com/scottphilip/google-token',
    author='Scott Philip',
    author_email='sp@scottphilip.com',
    packages=['GoogleToken'],
    version='0.7.6',
    install_requires=read('REQUIREMENTS.txt').splitlines(),
    license='GNU (v3) License',
    keywords=['Google Account', 'Access Token', 'oauth2', 'Automation'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
