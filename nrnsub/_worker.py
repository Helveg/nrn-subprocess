import nrnsub, sys, traceback
from tblib import pickling_support

pickling_support.install()

path_instructions = eval(sys.argv[2])
sys.path.extend(path_instructions)
f, args, kwargs = nrnsub._unpack_worker_data(sys.argv[1])
try:
    r = f(*args, **kwargs)
except Exception as e:
    try:
        e.test_str = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
        e.saved_traceback = e.__traceback__
        nrnsub._write_worker_error(e)
        exit(1)
    except Exception as ex:
        nrnsub._write_worker_error(ex)
        exit(1)
else:
    nrnsub._write_worker_result(r)
