# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="social.eusign",
    version='0.1',
    url='https://github.com/dstucrypt/social.eusign',
    description='python-social-auth plugin for EUSign.org',
    author='Ilya Petrov, Mikhail Kashkin',
    author_email='mkashkin@gmail.com',
    packages=find_packages('.'),
    namespace_packages=['social', ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'requests'
    ],
    license='BSD',
    classifiers=[
        'Topic :: Internet',
        'License :: OSI Approved :: BSD License',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
