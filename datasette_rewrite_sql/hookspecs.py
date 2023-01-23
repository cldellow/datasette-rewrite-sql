from pluggy import HookspecMarker

hookspec = HookspecMarker("datasette")


@hookspec
def rewrite_sql(datasette, database, fn, sql, params):
    "Inspect or rewrite the SQL request."
