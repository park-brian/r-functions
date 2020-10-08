import json
from asyncio.subprocess import create_subprocess_exec
from os import path
from subprocess import PIPE, run as run_subprocess
from tempfile import TemporaryDirectory
from typing import Any

# executes a function from the specified source file
r_source = """
args = commandArgs(trailingOnly = TRUE)
source_file <- args[1]
function_name <- args[2]
function_arguments_file <- args[3]
output_file <- args[4]

source(source_file)
function_arguments <- list()
if (file.exists(function_arguments_file))
    function_arguments <- as.list(jsonlite::read_json(function_arguments_file))
output <- do.call(function_name, function_arguments)
jsonlite::write_json(output, output_file, auto_unbox=TRUE, force = TRUE, na = "null")
"""


def run(
    source_file: str,
    function_name: str,
    arguments: Any = None,
    process_arguments: dict = {},
) -> Any:
    """
    Calls an R function from a source file and returns its output. If the
    function does not return a serializable value, stdout is returned.

    Keyword arguments:
    - source_file -- Path to the R source file
    - function_name -- Name of the R function to execute
    - arguments -- Arguments to apply to the R function - use a list for positional
      arguments or a dict for named arguments.
    - process_arguments -- Additional arguments passed to the R subprocess

    Returns:
        The R function's output
    """

    with TemporaryDirectory() as temp_dir:
        r_file = path.join(temp_dir, "source.R")
        input_file = path.join(temp_dir, "input.json")
        output_file = path.join(temp_dir, "output.json")

        with open(r_file, "w") as fp:
            fp.write(r_source)

        if arguments is not None:
            with open(input_file, "w") as fp:
                json.dump(arguments, fp)

        subprocess_arguments = {
            "check": True,
            "stdout": PIPE,
            "stderr": PIPE,
            **process_arguments,
        }
        stdout = run_subprocess(
            [
                "Rscript",
                r_file,
                source_file,
                function_name,
                input_file,
                output_file,
            ],
            **subprocess_arguments
        )

        if path.exists(output_file):
            with open(output_file) as fp:
                return json.load(fp)
        else:
            return stdout


async def run_async(
    source_file: str,
    function_name: str,
    arguments: Any = None,
    process_arguments: dict = {},
) -> Any:
    """
    Calls an R function from a source file asynchronously and returns its output.
    If the function does not return a serializable value, stdout is returned.

    Keyword arguments:
    - source_file -- Path to the R source file
    - function_name -- Name of the R function to execute
    - arguments -- Arguments to apply to the R function - use a list for positional
      arguments or a dict for named arguments.
    - process_arguments -- Additional arguments passed to the R subprocess

    Returns:
        The R function's output
    """

    with TemporaryDirectory() as temp_dir:
        r_file = path.join(temp_dir, "source.R")
        input_file = path.join(temp_dir, "input.json")
        output_file = path.join(temp_dir, "output.json")

        with open(r_file, "w") as fp:
            fp.write(r_source)

        if arguments is not None:
            with open(input_file, "w") as fp:
                json.dump(arguments, fp)

        subprocess_arguments = {"stdout": PIPE, "stderr": PIPE, **process_arguments}
        proc = await create_subprocess_exec(
            "Rscript",
            r_file,
            source_file,
            function_name,
            input_file,
            output_file,
            **subprocess_arguments
        )
        returncode = await proc.wait()
        stdout, stderr = await proc.communicate()

        if returncode != 0:
            raise Exception(
                {
                    "returncode": returncode,
                    "output": stdout,
                    "stdout": stdout,
                    "stderr": stderr,
                }
            )

        if path.exists(output_file):
            with open(output_file) as fp:
                return json.load(fp)
        else:
            return stdout


def create(source_file: str, function_name: str):
    """
    Creates a python function bound to an R function from a source file. The function
    may be called with either positional or named arguments, but not both.

    Keyword arguments:
    - source_file -- Path to the R source file
    - function_name -- Name of the R function to execute

    Returns:
        A bound function
    """

    return lambda *args, **kwargs: run(
        source_file, function_name, args if args else kwargs
    )


def create_async(source_file: str, function_name: str):
    """
    Creates an async python function bound to an R function from a source file. The function
    may be called with either positional or named arguments, but not both.

    Keyword arguments:
    - source_file -- Path to the R source file
    - function_name -- Name of the R function to execute

    Returns:
        A bound function
    """

    return lambda *args, **kwargs: run_async(
        source_file, function_name, args if args else kwargs
    )
