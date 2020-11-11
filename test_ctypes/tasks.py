import invoke

@invoke.task()
def build_cmult(c, path=None):
    """ Build the shared library for the sample C code """
    # Moving this type hint into signature causes an error (???)
    c: invoke.Context
    print("Building C Library")
    invoke.run("gcc -c -Wall -Werror -fpic cmult.c -I /usr/include/python3.7")
    invoke.run("gcc -shared -o libcmult.so cmult.o")
    print("* Complete")

@invoke.task()
def test_ctypes(c):
    """ Run the script to test ctypes """
    print("Testing ctypes Module")
    invoke.run("python3 ctypes_test.py", pty=True)
