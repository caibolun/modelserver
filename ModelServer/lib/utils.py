#coding=utf-8

import os
import sys
import pwd
import grp
import fcntl
import logging


from ModelServer.lib.errors import AppImportError

REDIRECT_TO=getattr(os, 'devnull', '/dev/null')

def daemonize(enable_stdio_inheritance=False):
    """
    Standard daemonize process.
    https://github.com/actberw/note/blob/master/linux/daemon-process.md
    """
    if os.fork():
        os._exit(0)

    os.setsid()
    os.umask(0)
    os.chdir('/')

    if os.fork():
        os._exit(0)

    if not enable_stdio_inheritance:
        # close stdin, stdout, stderr
        os.closerange(0, 3)

        fd_null = os.open(REDIRECT_TO, os.O_RDWR)
        if fd_null != 0:
            os.dup2(fd_null, 0)

        os.dup2(fd_null, 1)
        os.dup2(fd_null, 2)

    else:
        fd_null = os.open(REDIRECT_TO, os.O_RDWR)
        if fd_null != 0:
            os.close(0)
            os.dup2(fd_null, 0)


        def redirect(stream, fd_expect):
            try:
                fd = stream.fileno()
                if fd == fd_expect and stream.isatty():
                    os.close(fd)
                    os.dup2(fd_null, fd_expect)
            except AttributeError:
                pass

        redirect(sys.stdout, 1)
        redirect(sys.stderr, 2)

try:
    from setproctitle import setproctitle
    def _setproctitle(title):
        setproctitle(title)
except ImportError:
    def _setproctitle(title):
        return

def getcwd():
    # get current path, try to use PWD env first
    try:
        a = os.stat(os.environ['PWD'])
        b = os.stat(os.getcwd())
        if a.st_ino == b.st_ino and a.st_dev == b.st_dev:
            cwd = os.environ['PWD']
        else:
            cwd = os.getcwd()
    except:
        cwd = os.getcwd()
    return cwd

def set_process_owner(uid, gid):
    """ Set user and group of workers processes:
    Must setgid before uid, or permission denied.
    """
    gid = abs(gid) & 0x7FFFFFFF
    os.setgid(gid)
    os.setuid(uid)

def get_user_info(username, groupname):
    gid = grp.getgrnam(groupname).gr_gid
    uid = pwd.getpwnam(username).pw_uid
    return uid, gid

def close_on_exec(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFD)
    flags |= fcntl.FD_CLOEXEC
    fcntl.fcntl(fd, fcntl.F_SETFD, flags)

def set_non_blocking(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFL) | os.O_NONBLOCK
    fcntl.fcntl(fd, fcntl.F_SETFL, flags)

def reopen_log_file(logger):
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.acquire()
            try:
                if handler.stream:
                    handler.stream.close()
                    handler.stream = open(handler.baseFilename,
                                          handler.mode)
                    close_on_exec(handler.stream.fileno())
            finally:
                handler.release()

def chown(path, uid, gid):
    gid = abs(gid) & 0x7FFFFFFF  # see note above.
    os.chown(path, uid, gid)


def str2bool(value):
    _boolean_states = {'1': True, 'yes': True, 'true': True, 'on': True,
                       '0': False, 'no': False, 'false': False, 'off': False}
    return _boolean_states[value.lower()]

def first(iterable, key, default=None):
    for i in iterable:
        m = key(i)
        if m:
            return m
    else:
        return default

def import_app(module):
    parts = module.split(":", 1)
    if len(parts) == 1:
        module, obj = module, "run"
    else:
        module, obj = parts[0], parts[1]

    try:
        __import__(module)
    except ImportError:
        if module.endswith(".py") and os.path.exists(module):
            raise ImportError("Failed to find application, did "
                "you mean '%s:%s'?" % (module.rsplit(".", 1)[0], obj))
        else:
            raise

    mod = sys.modules[module]

    try:
        app = eval(obj, mod.__dict__)
    except NameError:
        raise AppImportError("Failed to find application: %r" % module)

    if app is None:
        raise AppImportError("Failed to find application object: %r" % obj)

    if not callable(app):
        raise AppImportError("Application object must be callable.")
    return app
