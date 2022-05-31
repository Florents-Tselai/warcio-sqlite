from setuptools import setup, find_packages
import io
import os

VERSION = "0.1.0"


def get_long_description():
    with io.open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
            encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="warcio-sqlite",
    description="CLI tool to load .warc files into SQLite",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Florents Tselai",
    version=VERSION,
    license="Apache License, Version 2.0",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "sqlite-utils==3.26.1",
        "warcio==1.7.4",
        "click==8.1.3"
    ],
    entry_points="""
        [console_scripts]
        warcio-sqlite=warcio_sqlite:cli
    """,
    url="https://github.com/Florents-Tselai/warcio-sqlite",
    project_urls={
        "Source code": "https://github.com/Florents-Tselai/warcio-sqlite",
        "Issues": "https://github.com/Florents-Tselai/warcio-sqlite/issues",
        "CI": "https://github.com/Florents-Tselai/warcio-sqlite/actions",
    },
    python_requires=">=3.6",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ]
)