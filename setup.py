import subprocess

import setuptools

# This will fail if something happens or if not in a git repository.
# This is intentional.
try:
    ret = subprocess.run(
        "git describe --tags --abbrev=0",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        shell=True,
    )
    version = ret.stdout.decode("utf-8").strip()
except:
    version = "main"

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setuptools.setup(
    name="sphinxext-opengraph",
    version=version,
    author="Itay Ziv",
    author_email="itay220204@gmail.com",
    description="Sphinx Extension to enable OGP support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wpilibsuite/sphinxext-opengraph",
    install_requires=["sphinx>=2.0"],
    packages=["sphinxext/opengraph"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Plugins",
        "Environment :: Web Environment",
        "Framework :: Sphinx :: Extension",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
)
