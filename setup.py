from setuptools import setup

with open("README.md") as fh:
    long_description = fh.read()

setup(
    name="r-functions",
    version="1.0.3",
    author="re.public",
    author_email="re.public@outlook.com",
    description="A library for running R functions from a source file",
    keywords="R, function, wrapper, library, async",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/park-brian/r-functions",
    py_modules=["r_functions"],
    test_suite="test",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    zip_safe=True,
)
