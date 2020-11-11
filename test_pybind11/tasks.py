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
def build_pybind11(c):
    """ Build the pybind11 wrapper library """
    print("Building PyBind11 Module")
    invoke.run(
        "g++ -O3 -Wall -Werror -shared -std=c++11 -fPIC "
        "`python3 -m pybind11 --includes` "
        "-I /usr/include/python3.7 -I .  "
        "{0} "
        "-o {1}`python3.7-config --extension-suffix` "
        "-L. -lcppmult -Wl,-rpath,.".format("pybind11_wrapper.cpp", "pybind11_example")
    )
    print("* Complete")

@invoke.task()
def test_pybind11(c):
    """ Run the script to test PyBind11 """
    print("Testing PyBind11 Module")
    invoke.run("python3 pybind11_test.py", pty=True)
