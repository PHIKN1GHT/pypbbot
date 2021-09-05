import os
import sys

import setuptools  # type: ignore

with open(os.path.join("pypbbot", "VERSION")) as f:
    __version__ = f.read()
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pypbbot",
    version=__version__,
    author="Kale1d0",
    author_email="kale1d0@qq.com",
    description="Python implementation for ProtobufBot Server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PHIKN1GHT/pypbbot",
    packages=setuptools.find_packages(include="pypbbot"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'pypbbot = pypbbot.serve:serve',
        ],
    },
    install_requires=[
        "psutil>=5.8.0",
        "uvicorn>=0.13.3",
        "loguru>=0.5.3",
        "fastapi>=0.63.0",
        "protobuf>=3.14.0",
        'returns>=0.15.0'
    ]
)
