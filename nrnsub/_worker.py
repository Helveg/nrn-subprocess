import nrnsub, sys, traceback
from tblib import pickling_support

pickling_support.install()

path_instructions = eval(sys.argv[2])
sys.path.extend(path_instructions)
try:
    f, args, kwargs = nrnsub._unpack_worker_data(sys.argv[1])
except Exception as e:
    og_msg = traceback.format_exception_only(type(e), e)[0][:-1]
    try:
        raise RuntimeError(f"Could not unpack worker data due to\n  {og_msg}")
    except Exception as e:
        nrnsub._write_worker_error(e)
        exit(1)
try:
    r = f(*args, **kwargs)
    nrnsub._write_worker_result(r)
except Exception as e:
    nrnsub._write_worker_error(e)
    exit(1)
