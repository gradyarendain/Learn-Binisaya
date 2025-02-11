from setuptools import setup, find_packages

setup(
    name="learn-binisaya",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'kuan=kuan_main:main',
        ],
    },
)
