from datasette import hookimpl

@hookimpl
def rewrite_sql(sql):
    if sql == 'SELECT 123':
        return 'SELECT 234'
    return sql
