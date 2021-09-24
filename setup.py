from setuptools import setup
import polydown.__main__ as m

with open("README.md", "r", encoding="UTF8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as file:
    requires = [line.strip() for line in file.readlines()]

VERSION = m.__version__
DESCRIPTION = "Batch downloader for polyhaven (polyhaven.com)."

setup(
    name="polydown",
    version=VERSION,
    url="https://github.com/agmmnn/polydown",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="agmmnn",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Topic :: Utilities",
    ],
    packages=["polydown"],
    install_requires=requires,
    include_package_data=True,
    package_data={"polydown": ["polydown/*"]},
    python_requires=">=3.5",
    entry_points={"console_scripts": ["polydown = polydown.__main__:cli"]},
)
