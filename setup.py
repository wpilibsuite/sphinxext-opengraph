import setuptools

with open("README.md", encoding="utf-8") as readme:
    long_description = readme.read()

setuptools.setup(
    name="sphinxext-opengraph",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    author="Itay Ziv",
    author_email="itay220204@gmail.com",
    description="Sphinx Extension to enable OGP support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wpilibsuite/sphinxext-opengraph",
    license="LICENSE.md",
    install_requires=["sphinx>=4.0", "matplotlib"],
    packages=["sphinxext/opengraph"],
    include_package_data=True,
    package_data={"sphinxext.opengraph": ["sphinxext/opengraph/_static/*"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Plugins",
        "Environment :: Web Environment",
        "Framework :: Sphinx :: Extension",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
)
