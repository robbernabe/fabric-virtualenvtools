import os
from functools import wraps
from fabric.api import env, prefix, cd

env.app_user = 'vagrant'
env.app_root = '/home/%s' % env.app_user
env.app_path = 'app/'
env.venv_path = 'venv/'


def get_virtualenv_path():
    return os.path.join(env.app_root, '%s/bin/activate' % env.venv_path)


def get_app_path():
    return os.path.join(env.app_root, env.app_path)


def virtualenv():
    """
    Fabric Context manager for use with 'with' statement.  Use it to
    perform actions with virtualenv activated like so:

        with virtualenv():
            run('pip install ..')
    """
    virtualenv_path = get_virtualenv_path()
    return prefix('source %s' % virtualenv_path)


def inside_virtualenv(func):
    """
    Decorator for use with tasks that need to be run inside a virtual environment:

        @inside_virtualenv
        def my_task():
            # virtual environment is activated here
    """
    @wraps(func)
    def inner(*args, **kwargs):
        with virtualenv():
            return func(*args, **kwargs)
    return inner


def inside_project(func):
    """
    Decorator for use with tasks that need to be run inside your project AND
    with the virtual environment activated:

        @inside_project
        def syncdb():
            # virtual environment is activated
            # in the root of the project
            run('python manage.py cleanup')
    """
    @wraps(func)
    def inner(*args, **kwargs):
        with cd(get_app_path()):
            with virtualenv():
                return func(*args, **kwargs)
    return inner
