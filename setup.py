# coding:utf-8

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    'chromedriver-binary',
    'selenium',
    'pywin32',
]

setuptools.setup(
    name="somed_rtc",
    version="0.2.4",
    author="Shih-Po Wang",
    author_email="sibo.wang@ot.olympus.co.jp",
    description="The Python binding Mantis SOAP API",
    install_requires=install_requires,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
