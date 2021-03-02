# NEURON subprocessing

Run multiple NEURON setups isolated from each other from a single Python script.
This package uses Python's `subprocess` to run multiple NEURON instances that
are completely seperated from eachother, making it easier to executed repeated
and parametrized simulations without having to worry about cleaning up the state
of the previous run.

## Installation

```
pip install nrn-subprocess
```

## Usage

Write your entire NEURON setup that you'd like to isolate inside of a function,
then use the `subprocess` or `isolate` approach to execute it in isolation:

### `subprocess`

```
import nrnsub

def my_sim(param1, opt1=None):
  from neuron import h
  s = h.Section(name="main")
  # ...
  return s.v

for i in range(10):
  nrnsub.subprocess(my_sim, 15, opt1=i)
```

This will run the subprocesses in series, parallel coming Soon (tm).

### `isolate`

There's also the `isolate` decorator that will make sure every call to that function is
ran as an isolated subprocess:

```
import nrnsub

@nrnsub.isolate
def my_sim(param1, opt1=None):
  from neuron import h
  s = h.Section(name="main")
  # ...
  return s.v

for i in range(10):
  my_sim(15, opt1=i)
```

## Worker `PATH`

The worker might have trouble unpacking the serialized objects because it can't
find the module they came from on the main process. This might result in `dill`
raising "module not found" errors. To fix them you can pass the `_worker_path` to
`subprocess` or `worker_path` to the `isolate` decorator:

```
import nrnsub

sys.path.insert(0, "/home/me/my_modules_folder")

@nrnsub.isolate(worker_path=["/home/me/my_modules_folder"])
def f():
  import something_in_my_modules_folder
```
