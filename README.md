# datasette-rewrite-sql

[![PyPI](https://img.shields.io/pypi/v/datasette-rewrite-sql.svg)](https://pypi.org/project/datasette-rewrite-sql/)
[![Changelog](https://img.shields.io/github/v/release/cldellow/datasette-rewrite-sql?include_prereleases&label=changelog)](https://github.com/cldellow/datasette-rewrite-sql/releases)
[![Tests](https://github.com/cldellow/datasette-rewrite-sql/workflows/Test/badge.svg)](https://github.com/cldellow/datasette-rewrite-sql/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/cldellow/datasette-rewrite-sql/blob/main/LICENSE)

Adds a rewrite_sql hook to Datasette

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-rewrite-sql

## Usage

Write a hook like:

```python
from datasette import hookimpl

@hookimpl
def rewrite_sql(sql):
  if sql == 'select 123':
    return 'select 234'

  return sql
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-rewrite-sql
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
