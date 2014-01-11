import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-easy-timezones',
    version='0.2.0',
    packages=['easy_timezones'],
    install_requires=[
        "pygeoip",
        "pytz",
    ],
    include_package_data=True,
    license='Apache License',
    description='Easy timezones for Django (>=1.4) based on MaxMind GeoIP.',
    long_description=README,
    url='https://github.com/Miserlou/django-easy-timezones',
    author='Rich Jones',
    author_email='rich@openwatch.net',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
