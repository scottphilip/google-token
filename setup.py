from setuptools import setup

setup(
    name='GoogleToken',
    description='Google User Account login automation',
    url='http://github.com/scottphilip/google-token',
    author='Scott Philip',
    author_email='sp@scottphilip.com',
    packages=['GoogleToken'],
    version='0.5',
    install_requires=['selenium', 'pyotp'],
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
    ],
)
