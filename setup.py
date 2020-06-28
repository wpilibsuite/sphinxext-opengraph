import subprocess

import setuptools

# This will fail if something happens or if not in a git repository.
# This is intentional.
ret = subprocess.run("git describe --tags --abbrev=0", stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, check=True, shell=True)
version = ret.stdout.decode("utf-8").strip()

with open("readme.md", 'r') as readme:
    long_description = readme.read()

setuptools.setup(
    name="wpilib-ogp",
    version=version,
    author="Itay Ziv",
    author_email="itay220204@gmail.com",
    description="Sphinx Extension to enable OGP support",
    long_descrption=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wpilibsuite/ogp",
    packages=['wpilib'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Framework :: Sphinx :: Extension",
    ],
    python_requires='>=3.6'
)
