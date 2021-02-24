import nrnsub, sys

f, args, kwargs = nrnsub._unpack_worker_data(sys.argv[1])
nrnsub._write_worker_result(f(*args, **kwargs))
