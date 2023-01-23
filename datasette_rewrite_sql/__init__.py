from datasette.utils import await_me_maybe
from datasette import hookimpl
from datasette.plugins import pm
from datasette.database import Database
from . import hookspecs

original_execute = Database.execute
original_execute_write = Database.execute_write
original_execute_write_script = Database.execute_write_script
original_execute_write_many = Database.execute_write_many

async def patched_execute(
    self,
    sql,
    params=None,
    truncate=False,
    custom_time_limit=None,
    page_size=None,
    log_sql_errors=True,
):
    rewritten = await rewrite(self.ds, self, 'execute', sql, params)
    return await original_execute(
        self,
        rewritten,
        params,
        truncate,
        custom_time_limit,
        page_size,
        log_sql_errors
    )

async def patched_execute_write(self, sql, params=None, block=True):
    rewritten = await rewrite(self.ds, self, 'execute_write', sql, params)

    return await original_execute_write(self, rewritten, params, block)

async def patched_execute_write_script(self, sql, block=True):
    rewritten = await rewrite(self.ds, self, 'execute_write_script', sql, None)

    return await original_execute_write_script(self, rewritten, block)

async def patched_execute_write_many(self, sql, params_seq, block=True):
    rewritten = await rewrite(self.ds, self, 'execute_write_many', sql, params_seq)
    return await original_execute_write_many(self, rewritten, params_seq, block)

Database.execute = patched_execute
Database.execute_write = patched_execute_write
Database.execute_write_many = patched_execute_write_many
Database.execute_write_script = patched_execute_write_script


@hookimpl
def startup():
    pm.add_hookspecs(hookspecs)

async def rewrite(datasette, database, fn, sql, params):
    # A challenge: if two plugins are participating in rewriting, who wins?
    #
    # Option 1: the first one registered wins.
    # Option 2: the output of the first is fed into the second.
    #
    # With option 2, if two plugins rewrite the output, ought the first one
    # get another kick at the can to rewrite the output of the second? That is,
    # should rewrites continue until no plugin wants to rewrite again?
    #
    # That feels like the "right" solution, but is probably hard for programmers
    # to reason about -- I can imagine easily getting into an infinite loop.
    #
    # Instead, let's let each hook rewrite exactly once.
    #
    # This seems to not be a supported case for pluggy. So, let's do
    # some vaguely evil things to do it ourselves.
    caller_kwargs = {
        'datasette': datasette,
        'database': database,
        'fn': fn,
        'sql': sql,
        'params': params
    }

    for hook_impl in pm.hook.rewrite_sql.get_hookimpls():
        args = [caller_kwargs[argname] for argname in hook_impl.argnames]
        res = await await_me_maybe(hook_impl.function(*args))

        if res is not None:
            sql = res
            caller_kwargs['sql'] = sql

    return sql
