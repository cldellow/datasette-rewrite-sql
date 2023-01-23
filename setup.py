from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-rewrite-sql",
    description="Adds a rewrite_sql hook to Datasette",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Colin Dellow",
    url="https://github.com/cldellow/datasette-rewrite-sql",
    project_urls={
        "Issues": "https://github.com/cldellow/datasette-rewrite-sql/issues",
        "CI": "https://github.com/cldellow/datasette-rewrite-sql/actions",
        "Changelog": "https://github.com/cldellow/datasette-rewrite-sql/releases",
    },
    license="Apache License, Version 2.0",
    classifiers=[
        "Framework :: Datasette",
        "License :: OSI Approved :: Apache Software License"
    ],
    version=VERSION,
    packages=["datasette_rewrite_sql"],
    entry_points={"datasette": ["rewrite_sql = datasette_rewrite_sql"]},
    install_requires=["datasette"],
    extras_require={"test": ["pytest", "pytest-asyncio", "pytest-watch"]},
    python_requires=">=3.7",
)
