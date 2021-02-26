"""
Facilitates the isolation of NEURON simulators by running them in subprocesses.
"""

import os
import sys
import codecs
import inspect
import functools
import subprocess as _sp
import dill


_worker_script = os.path.join(os.path.dirname(__file__), "_worker.py")
_boundary = "|!|!|!|!|!|!|!|!|!|"
_boundary_bytes = bytes(_boundary, "utf-8")

def _get_obj_module_path(obj):
    p = inspect.getfile(obj)
    print("FOUND PATH:", p)
    d = os.path.dirname(p)
    if p.endswith("__init__.py"):
        return os.path.dirname(d)
    return d

def subprocess(f, *args, _worker_path=None, **kwargs):
    if _worker_path is None:
        _worker_path = []
    result = _invoke(f, args, kwargs, _worker_path)
    return result

def _invoke(f, args, kwargs, paths):
    objstr = _obj2str((f, args, kwargs))
    try:
        out = _sp.check_output([sys.executable, _worker_script, objstr, repr(paths)])
    except _sp.CalledProcessError as e:
        print(e.output)
    else:
        return _unpack_worker_result(out)

def _obj2str(obj):
    dillbytes = dill.dumps(obj)
    return codecs.encode(dillbytes, "base64").decode("utf-8")

def _b64bytes2obj(b64bytes):
    dillbytes = codecs.decode(b64bytes, "base64")
    return dill.loads(dillbytes)

def _unpack_worker_data(data):
    b64bytes = bytes(data, "utf-8")
    return _b64bytes2obj(b64bytes)

def _write_worker_result(result):
    sys.stdout.write(_boundary + _obj2str(result) + _boundary)

def _unpack_worker_result(result):
    c = result.count(_boundary_bytes)
    if c != 2:
        raise RuntimeError(f"Subprocess communication error. Received {c} data boundary signals, expected 2.")
    b64bytes = result.split(_boundary_bytes)[1]
    bytestream = codecs.decode(b64bytes, "base64")
    return dill.loads(bytestream)

def isolate(f=None, worker_path=None):
    """
    Decorator to run the decorated function in an isolated subprocess.
    """
    @functools.wraps(f)
    def subprocessor(*args, **kwargs):
        return subprocess(f, *args, _worker_path=worker_path, **kwargs)
    if f is not None:
        return subprocessor
    def decorator(f_inner):
        nonlocal f
        f = f_inner
        return subprocessor
    return decorator
