# r-functions
`r-functions` is a small library which allows users to call R functions from within Python. Each function runs in a temporary R subprocess which exits upon completion. An async version is provided for concurrent execution.

Consider using Apache Arrow to transfer large datasets between Python and R, as parameters and return values are serialized in memory as JSON. 

### Prerequisites
- Python 3.6+
- R 3/4.0+
  - jsonlite


### Installation
Ensure that RScript is in your `PATH` and jsonlite is installed.

```bash
# install jsonlite
Rscript -e "install.packages('jsonlite', repos='https://cloud.r-project.org/', lib = .Library)"

# or pip3, depending on your platform
pip install r-functions 
```

### Example file: _test.R_
```R
add <- function(a, b) {
    a + b
}

greet <- function(name, adjective) {
    paste("Hello", name, "the", adjective)
}
```

### Example: run functions from _test.R_
```python
from r_functions import create, run

# create Python functions bound to R functions
add = create("test.R", "add")
greet = create("test.R", "greet")

sum = add(2, 3)
print(sum) # 5

# we can use named parameters or positional parameters, but not both
greeting = greet(name="John", adjective="Wise")
print(greeting) # "Hello John the Wise"

# alternatively, use r_functions.run

# lists provide positional parameters
sum = run("test.R", "add", [2, 3])

# dicts provide named parameters
greeting = run("test.R", "greet", {
    "name": "John",
    "adjective": "Wise",
})

# optionally, provide subprocess options
# https://docs.python.org/3/library/subprocess.html#frequently-used-arguments
run("test.R", "add", [1, 2], {
    "cwd": None, 
    "env": None, 
    "input": None, 
    "stdout": None, 
    "stderr": None, 
    # ...
})
```


### Example: run functions from _test.R_ asynchronously
```python
import asyncio
import sys
from r_functions import create_async, run_async

# on Windows, we must use the ProactorEventLoop to support subprocesses
# https://docs.python.org/3.6/library/asyncio-subprocess.html#windows-event-loop
if sys.platform == "win32":
    asyncio.set_event_loop(asyncio.ProactorEventLoop())

async def main():

    # create async Python functions bound to R functions
    add = create_async("test.R", "add")
    greet = create_async("test.R", "greet")

    sum = await add(2, 3)
    print(sum) # 5

    # we can use named parameters or positional parameters, but not both
    greeting = await greet(name="John", adjective="Wise")
    print(greeting) # "Hello John the Wise"

    # alternatively, use r_functions.run

    # lists provide positional parameters
    sum = await run_async("test.R", "add", [2, 3])

    # dicts provide named parameters
    greeting = await run_async("test.R", "greet", {
        "name": "John",
        "adjective": "Wise",
    })

    # optionally, provide subprocess options - by default, stdout/stderr use subprocess.PIPE
    # https://docs.python.org/3.6/library/asyncio-subprocess.html#asyncio.AbstractEventLoop.subprocess_exec
    await run_async("test.R", "add", [1, 2], {
        "cwd": None, 
        "env": None, 
        "stdout": None, 
        "stderr": None, 
        "limit": None, 
        # ...
    })

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```


### Notes
When running async R functions on Windows, you must use the ProactorEventLoop to support subprocesses. 
For example:

```python
import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop(asyncio.ProactorEventLoop())
```

When supplying custom environmental variables to an R subprocess, you must include a valid PATH which contains the R executable. On Windows, a SYSTEMROOT (usually "C:\Windows" or simply `%SystemRoot%`) must also be provided. 

Specifying custom environmental variables for R can be useful if global changes are not desired, or if the user wishes to use a different version of R without reconfiguring their PATH.

For example:


```R
get_env <- function(name) {
    Sys.getenv(name)
}
```

```python
import os
from r_functions import run

# on Posix-like systems
test_value = run("test.R", "get_env", {"name": "test"}, {
    "shell": True,
    "env": {
        "test": "test_value", 
        "PATH": "/opt/R-$VERSION/bin",
        "R_PROFILE": "/opt/R-$VERSION/etc/Rprofile.site",
        "R_LIBS": "/opt/R-$VERSION/library",
    }
})

# on Windows
test_value = run("test.R", "get_env", {"name": "test"}, {
    "shell": True,
    "env": {
        "test": "test_value", 
        "PATH": "X:\\R-$VERSION\\bin"
        "R_PROFILE": "X:\\R-$VERSION\\etc\\Rprofile.site",
        "R_LIBS": "X:\\R-$VERSION\\library"
        "SYSTEMROOT": os.path.expandvars("%SystemRoot%"), 
    }
})
```