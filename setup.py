import os
import sys

import setuptools  # type: ignore

import pypbbot

sys.path.insert(0, os.path.abspath('src'))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pypbbot",
    version=pypbbot.__version__,
    author="Kale1d0",
    author_email="kale1d0@qq.com",
    description="Python implementation for ProtobufBot Server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PHIKN1GHT/pypbbot",
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "uvicorn>=0.13.3",
        "loguru>=0.5.3",
        "fastapi>=0.63.0",
        "protobuf>=3.14.0",
        'returns>=0.15.0'
    ]
)
