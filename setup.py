import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytoniq-tools",
    version="0.0.5",
    author="nessshon",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nessshon/pytoniq-tools/",
    packages=setuptools.find_packages(exclude=["examples"]),
    install_requires=[
        "pytoniq~=0.1.39",
        "pytoncenter~=0.0.14",
        "pytonapi~=0.3.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
