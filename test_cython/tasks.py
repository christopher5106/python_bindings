import invoke

@invoke.task()
def build_cppmult(c):
    """ Build the shared library for the sample C++ code """
    print("Building C++ Library")
    invoke.run(
        "g++ -O3 -Wall -Werror -shared -std=c++11 -fPIC cppmult.cpp "
        "-o libcppmult.so "
    )
    print("* Complete")

@invoke.task(build_cppmult)
def build_cython(c):
    """ Build the cython extension module """
    print("Building Cython Module")
    # Run cython on the pyx file to create a .cpp file
    invoke.run("cython --cplus -3 cython_example.pyx -o cython_wrapper.cpp")

    # Compile and link the cython wrapper library
    invoke.run(
        "g++ -O3 -Wall -Werror -shared -std=c++11 -fPIC "
        "`python3 -m pybind11 --includes` "
        "-I /usr/include/python3.7 -I .  "
        "{0} "
        "-o {1}`python3.7-config --extension-suffix` "
        "-L. -lcppmult -Wl,-rpath,.".format("cython_wrapper.cpp", "cython_example")
    )
    print("* Complete")


@invoke.task()
def test_cython(c):
    """ Run the script to test Cython """
    print("Testing Cython Module")
    invoke.run("python3 cython_test.py", pty=True)
