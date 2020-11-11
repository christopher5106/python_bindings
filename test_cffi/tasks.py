import invoke
import cffi
import pathlib

@invoke.task()
def build_cffi(c):
    """ Build the CFFI Python bindings """
    print("Building CFFI Module")
    invoke.run("gcc -c -Wall -Werror -fpic cmult.c -I /usr/include/python3.7")
    invoke.run("gcc -shared -o libcmult.so cmult.o")

    ffi = cffi.FFI()

    this_dir = pathlib.Path().resolve()
    h_file_name = this_dir / "cmult.h"
    with open(h_file_name) as h_file:
        ffi.cdef(h_file.read())

    ffi.set_source(
        "cffi_example",
        # Since we are calling a fully built library directly no custom source
        # is necessary. We need to include the .h files, though, because behind
        # the scenes cffi generates a .c file which contains a Python-friendly
        # wrapper around each of the functions.
        '#include "cmult.h"',
        # The important thing is to include the pre-built lib in the list of
        # libraries we are linking against:
        libraries=["cmult"],
        library_dirs=[this_dir.as_posix()],
        extra_link_args=["-Wl,-rpath,."],
    )

    ffi.compile()
    print("* Complete")


@invoke.task()
def test_cffi(c):
    """ Run the script to test CFFI """
    print("Testing CFFI Module")
    invoke.run("python cffi_test.py", pty=True)
