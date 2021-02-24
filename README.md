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

## Decorator

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
