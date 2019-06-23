#!/usr/bin/env/python3


""" contextlib - Context Manager Utilities """

# The contextlib module contains utilities for working with context managers and the "with" statement



""" Context Manager API """

# A context manager is responsible for a resource within a code block, possibly creating it when the block is entered
# and then cleaning it up after the block is exited. For example, files support the context manager API to make it easy
# to ensure they are closed after all reading or writing is done


with open("text.txt", "wt") as f:
    f.write("contents go here")


# A context manager is enabled by the with statement, and the APi involves two methods. The __enter__() method is run
# when execution flow enters the code block inside the with. It returns an object to be used within the context.
# When execution flow leaves the with block, the __exit__() method of the context manager is called to clean up any
# resources being used.

class Context:

    def __init__(self):
        print("__init__()")

    def __enter__(self):
        print("__enter__()")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("__exit__()")


with Context():
    print("Doing work in the context")

# Combining a context manager and the with statement is a more compact way of writing a try:finally block, since the
# context manager's __exit__() method is always called, even if an exception is raised.

# The __enter__() method can return any object to be associated with a name specified in the "as" clause of the with
# statement. In this example, the Context returns an object that uses the open context.

class WithinContext:

    def __init__(self, context):
        print("WithinContext.__init__({})".format(context))

    def do_something(self):
        print("WithinContext.do_something()")

    def __del__(self):
        print("WithinContext.__del__")


class Context:
    def __init__(self):
        print("Context.__init__()")

    def __enter__(self):
        print("Context.__enter__()")
        return WithinContext(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Context.__exit__()")


with Context() as c:
    c.do_something()

# The value associated with the variable c is the object returned by __enter__(), which is not necessarily the Context
# instance created in the with statement


# The __exit__() method receives arguments containing deatils of any exception raised in the with block

class Context:

    def __init__(self, handle_error):
        print("__init__({})".format(handle_error))
        self.handle_error = handle_error

    def __enter__(self):
        print("__enter__()")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("__exit__()")
        print("exc_type =", exc_type)
        print("exc_val  =", exc_val)
        print("exc_tb   =", exc_tb)
        return self.handle_error


with Context(True):
    raise RuntimeError("error message handled")

print()

#with Context(False):
#    raise RuntimeError("error message propagated")

# If the context manager can handle the exception, __exit__() should return a true value to indicate that the exception
# does not need to be propagated. Returning false causes the exception to be re-raised after __exit__() returns.


""" Context managers as function decorators"""

# The class ContextDecorator adds support to regular context manager classes to let them be used as function decorators
# as well as context managers.

import contextlib
class Context(contextlib.ContextDecorator):

    def __init__(self, how_used):
        self.how_used = how_used
        print("__init__({})".format(how_used))

    def __enter__(self):
        print("__enter__({})".format(self.how_used))

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("__exit__({})".format(self.how_used))


@Context("as decorator")
def func(message):
    print(message)

print()
with Context("as context manager"):
    print("Doing work in the context")

print()
func("Doing work in the wrapped function")
print()

# One difference with using the context manager as a decorator is that the value returned by __enter__() is not
# available inside the function being decorated, unlike when using with and as. Arguments passed to the decorated
# function are available in the usual way.


""" From Generator to Context Manager """

# Creating context managers the traditional way, by writing a class with __enter__() and __exit__() methods, is not
# difficult. But sometimes writing everything out fully is extra overhead for a trivial bit of context. In those sorts
# of situations, use the contextmanager() decorator to convert a generator function into a context manager.

@contextlib.contextmanager
def make_context():
    print(" entering")
    try:
        yield {}
    except RuntimeError as err:
        print(" ERROR: ", err)
    finally:
        print(" exiting")

print("Normal:")
with make_context() as value:
    print(" inside the statement:", value)

print("\nHandled error:")
with make_context() as value:
    raise RuntimeError("showing example of handling an error")

print("\nUnhandled error:")
#with make_context() as value:
    # raise ValueError("this exception is not handled")

# The generator should initialize the context, yield exactly one time, then clean up the context. The value yielded,
# if any, is bound to the variable in the "as" clause of the "with" statement. Exceptions from within the "with" block
# are re-raised inside the generator, so they can be handled there.from

# The context manager returned by contextmanager() is derived from ContextDecorator, so it also works as a function
# decorator.

@contextlib.contextmanager
def make_context():
    print('  entering')
    try:
        # Yield control, but not a value, because any value
        # yielded is not available when the context manager
        # is used as a decorator.
        yield
    except RuntimeError as err:
        print('  ERROR:', err)
    finally:
        print('  exiting')


@make_context()
def normal():
    print('  inside with statement')


@make_context()
def throw_error(err):
    pass
    #raise err


print('Normal:')
normal()

print('\nHandled error:')
throw_error(RuntimeError('showing example of handling an error'))

print('\nUnhandled error:')
throw_error(ValueError('this exception is not handled'))

# As in the ContextDecorator example above, when the context manager is used as a decorator the value yielded by the
# generator is not available inside the function being decorated. Arguments passed to the decorated function are still
# available, as demonstrated by throw_error() in this example.


""" Closing open handles """

# The file class supports the context manager API directly, but some other objects that represent open handles do not.
# The example given in the standard library documentation for contextlib is the object returned from urllib.urlopen().
# There are other legacy classes that use a close() method but do not support the context manager API. To ensure that
# handle is closed, use closing() to create a context manager for it.

class Door:

    def __init__(self):
        print(" __init__()")
        self.status = "open"

    def close(self):
        print(" close()")
        self.status = "closed"

print("Normal example:")
with contextlib.closing(Door()) as door:
    print(" inside with statement: {}".format(door.status))
print(" outside with statement: {}".format(door.status))

print("\nError handling example:")
try:
    with contextlib.closing(Door()) as door:
        print(" raising from inside with statement")
        raise RuntimeError("error message")
except Exception as err:
    print(" Had an error:", err)
print()
# The handle is closed whether there is an error in the "with" block or not.


""" Ignoring exceptions """

# It is frequently useful to ignore exceptions raised by libraries, because the error indicates that the desired state
# has already been achieved, or it can otherwise be ignored. The most common way to ignore exceptions is with a
# try:except statement with only a pass statement in the except block

class NonFatalError(Exception):
    pass

def non_idempotent_operation():
    raise NonFatalError(
        "The operation failed because of existing state"
    )

try:
    print("Trying non-idempotent operation")
    non_idempotent_operation()
    print("Succeeded!")
except NonFatalError:
    pass


# The try:except can be replaced with contextlib.suppress() to more explicitly suppress a class of exceptions happening
# anywhere in the "with" block

class NonFatalError(Exception):
    pass

def non_idempotent_operation():
    raise NonFatalError(
        "The operation failed because of the existing state"
    )


with contextlib.suppress(NonFatalError):
    print("Trying out non-idempotent operation")
    non_idempotent_operation()
    print("Succeeded!")

print("Done")


""" Redirecting output streams """

# Poorly designed library code may write directly to sys.stdout or sys.stderr, without providing arguments to configure
# different output destinations. The redirect_stdout() and redirect_stderr() context managers can be used to capture
# output from functions like this, for which the source cannot be changed to accept a new output argument

from contextlib import redirect_stderr, redirect_stdout
import io
import sys

def misbehaving_function(a):
    sys.stdout.write("(stdout) A: {!r}\n".format(a))
    sys.stderr.write("(stderr) A: {!r}\n".format(a))


capture = io.StringIO()
with redirect_stdout(capture), redirect_stderr(capture):
    misbehaving_function(5)

print(capture.getvalue())

# In this example misbehaving_function() writes to both stdout and sterr, but the two context managers send that
# output to the same io.StringIO instance where it is saved to be used later.

# Note:
# Both functions modify global state by replacing objects in the sys module, and should be used with care. The functions
# are not thread-safe, and may intefere with other operations that expect the standard output streams to be attached to
# terminal devices.


""" Dynamic context manager stacks """

# A program may need to create an unknown number of objects in a context, while wanting all of them to be cleaned up
# when control flow exits the context. ExitStack was created to handle these more dynamic cases.
# An ExitStack instance maintains a stack data structure of cleanup callbacks. The callbacks are populated explicitly
# within the context, and any registered callbacks are called in the reverse order when control flow exits the context.
# The result is like having multiple nested "with" statements , except they are established dynamically.

""" Stacking context managers """

# There are several ways to populate the ExitStack. This example uses enter_context() to add a new context manager to
# the stack.


@contextlib.contextmanager
def make_context(i):
    print("{} entering".format(i))
    yield {}
    print("{} exiting".format(i))


def variable_stack(n, msg):
    with contextlib.ExitStack() as stack:
        for i in range(n):
            stack.enter_context(make_context(i))
            print(msg)


variable_stack(5, "inside context")


# enter_context() first calls __enter__() on the context manager, and then registers its __exit__() method as a callback
# to be invoked as the stack is undone.

# The context managers given to ExitStack are treated as though they are in a series of nested "with" statements.
# Errors that happen anywhere within the context propagate through the normal error handling of the context managers.
# These context manager classes illustrate the way errors propagate.

class Tracker:
    " Base class for noisy context managers. "

    def __init__(self, i):
        self.i = i

    def msg(self, s):
        print(" {}({}): {}".format(
            self.__class__.__name__, self.i, s
        ))

    def __enter__(self):
        self.msg("Entering")


class HandleError(Tracker):
    " If an exception is received tread is as handled. "

    def __exit__(self, *exc_details):
        received_exc = exc_details[1] is not None
        if received_exc:
            self.msg("handling exception {!r}".format(
                exc_details[1]
            ))
        self.msg("exiting {}".format(received_exc))

        # return boolean value indicating whether the exception was handled
        return received_exc


class PassError(Tracker):
    " If an exception is received, propagate it. "

    def __exit__(self, *exc_details):
        received_exc = exc_details[1] is not None
        if received_exc:
            self.msg("passing exception {!r}".format(
                exc_details[1]
            ))
        self.msg("Exiting")
        # return False, indicating any exception was not handled
        return False


class ErrorOnExit(Tracker):
    " Cause an exception. "

    def __exit__(self, *exc_details):
        self.msg("Throwing error")
        raise RuntimeError("from {}".format(self.i))


class ErrorOnEnter(Tracker):
    " Cause an exception. "

    def __enter__(self):
        self.msg("Throwing error on enter")
        raise RuntimeError("from {}".format(self.i))

    def __exit__(self, *exc_info):
        self.msg("Exiting")

# The examples using these classes are based around variable_stack(), which uses the context managers passed to
# construct an ExitStack, building up the overall context one by one. The examples below pass different context
# managers to explore the error handling behavior. First, the normal case of no exceptions.
print()
myList = [HandleError(1), PassError(2), ]
def variable_stack(n, msg):
    with contextlib.ExitStack() as stack:
        for i in myList:
            stack.enter_context(make_context(i))
            print(msg)

print("No errors:")
variable_stack(myList, "Inside variable_stack_1")

# Then, an example of handling exceptions within the context managers at the end of the stack, in which all of the open
# contexts are closed as the stack is unwound.

print("\nError at the end of the context stack:")
myList_2 = [HandleError(1), HandleError(2), ErrorOnExit(3),]
def variable_stack(n, msg):
    with contextlib.ExitStack() as stack:
        for i in myList_2:
            stack.enter_context(make_context(i))
            print(msg)
variable_stack(myList_2, "Inside variable_stack_2")


# Next an example of handling exceptions within the context managers in the middle of the stack, in which the error does
# not occur until some context are already closed, so those contexts do not see the error.

print("\nError in the middle of the context stack:")
myList_3 = [HandleError(1), PassError(2), ErrorOnExit(3), HandleError(4),]
variable_stack(myList_3, "Inside variable_stack_3")


# Finally, an example of the exception remaining unhandled and propagating up to the calling code
myList_4 = [PassError(1), ErrorOnExit(2)]
try:
    print("\nError ignored:")
    variable_stack(myList_4, "Inside variable_stack_4")

except RuntimeError:
    print("error handled outside of context")
print()

# If any context manager in the stack receives an exception and returns a True value, it prevents that exception from
# propagating up to any other context managers.



""" Arbitrary context callbacks """

# ExitStack also supports arbitrary callbacks for closing a context, making it easy to clean up resources that are not
# controlled via a context manager.


def callback(*args, **kwds):
    print("Closing callback({}, {})".format(args, kwds))


with contextlib.ExitStack() as stack:
    stack.callback(callback, "arg1", "arg2")
    stack.callback(callback, arg3="val3")

# Just as with the __exit__() methods of full context managers, the callbacks are invoked in the reverse order that they
# are registered.

# The callbacks are invoked regardless of whether an error occurred, and they are not given any information about
# whether an error occurred. Their return value is ignored.

try:
    with contextlib.ExitStack() as stack:
        stack.callback(callback, "arg1", "arg2")
        stack.callback(callback, arg3="val3")
        raise RuntimeError("thrown error")

except RuntimeError as err:
    print("ERROR: {}".format(err))

# Because they do not have access to the error, callbacks are unable to suppress exceptions from propagating through
# the rest of the stack of context managers.

# Callbacks make a convenient way to clearly define cleanup logic without the overhead of creating a new context manager
# class. To improve code readability, that logic can be encapsulated in an inline function, and callback() can be used
# as a decorator.

with contextlib.ExitStack() as stack:

    @stack.callback
    def inline_cleanup():
        print("inline_cleanup()")
        print("local_resource = {!r}".format(local_resource))

    local_resource = " Resource created in context "
    print("Within the context")

# There is no way to specify the arguments for function registered using the decorator form of callback(). However, if
# the cleanup callback is defined inline, scope rules give it access to variables defined in the calling code.


""" Partial stacks """

# Sometimes when building complex contexts it is useful to be able to abort an operation if the context cannot be
# completely constructed, but to delay the cleanup of all resources until a later time if they can all be set up
# properly. For example, if an operation needs several long-lived network connections, it may be best to not start the
# operation if one connection fails. However, if all of the connections can be opened they need to stay open longer
# than the duration of a single context manager. The pop_all() method of ExitStack can be used in this scenario.

# pop_all() clears all of the context managers and callbacks from the stack on which it is called, and returns a new
# stack pre-populated with those same context managers and callbacks. The close() method of the new stack can be
# invoked later, after the original stack is gone, to clean up the resources.


def variable_stack(contexts):
    with contextlib.ExitStack() as stack:
        for c in contexts:
            stack.enter_context(c)
        # return the close() method of a new stack as a cleanup function
        return stack.pop_all().close

    return None

print("No errors:")

cleaner = variable_stack([
    HandleError(1),
    HandleError(2)
])
cleaner()

print("\nHandled error building context manager stack:")

try:
    cleaner = variable_stack([
        HandleError(1),
        ErrorOnEnter(2)
    ])

except RuntimeError as err:
    print("caught error {}".format(err))

else:
    if cleaner is not None:
        cleaner()

    else:
        print("no cleaner returned")


print("\nUnhandled error building context manager stack:")

try:
    cleaner = variable_stack([
        PassError(1),
        ErrorOnEnter(2)
    ])
except RuntimeError as err:
    print("caught error {}".format(err))

else:
    if cleaner is not None:
        cleaner()
    else:
        print("no cleaner returned")

# This example uses the same context manager classes defined earlier, with the difference that ErrorOnEnter produces
# an error on __enter__() instead of __exit__(). Inside variable_stack(), if all of the contexts are entered without
# error then the close() method of a new ExitStack is returned. If a handled error occurs, variable_stack() returns
# None to indicate that the cleanup work is already done. And if an unhandled error occurs, the partial stack is
# cleaned up and the error is propagated.

