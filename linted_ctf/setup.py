import io

from setuptools import find_packages, setup



setup(
    name='ezctf',
    version='1.0.0',
    url='ezctf.com',
    license='None',
    maintainer='floridaman',
    maintainer_email='',
    description='A simple CTF webapp.',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage'
        ],
    },
)
