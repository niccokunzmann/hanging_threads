hanging_threads
===============

Deadlocks? Detect where your threads hang in Python.

.. image:: https://travis-ci.org/niccokunzmann/hanging_threads.svg
   :target: https://travis-ci.org/niccokunzmann/hanging_threads
   :alt: Build Status

.. image:: https://badge.fury.io/py/hanging_threads.svg
   :target: https://pypi.python.org/pypi/hanging_threads
   :alt: Python Package Index

Install
-------

You can install the module with pip:

.. code:: bash

    pip install hanging_threads


If you are under **Windows**, you can open the command line program "cmd" and type

.. code:: bash

    py -m pip install hanging_threads


Usage
-----

Starting monitoring as simple as calling the start_monitoring() function.

.. code:: python

    from hanging_threads import start_monitoring
    monitoring_thread = start_monitoring()

You may also pass additional parameters.

.. code:: python

    monitoring_thread = start_monitoring(seconds_frozen=10, test_interval=100)

The values in the example are defaults. This mean the check will happen 10
times per second. If a thread is frozen for at least 10 seconds then the stack
is dumped into standard error stream. This happens again every 10 seconds
while there is no changes in the stack registered during checks. Checks are done in
intervals of 100ms.

Note that it makes sense to save the thread object into variable so that you or
somebody else can stop this annoying dumps if needed.
For example, you may want to do this in Python shell.

.. code:: python

    monitoring_thread.stop()



Useful Stackoverflow links
--------------------------

- `GIL-deadlocks are not covered by this <http://stackoverflow.com/questions/10014481/python-threads-hang#comment33263430_17744731>`__
- `Package requested, so this was created <http://stackoverflow.com/questions/3443607/how-can-i-tell-where-my-python-script-is-hanging/17744556#comment69129716_17744556>`__
