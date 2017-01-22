Notes on Development
====================

Deployment
----------

We have branches for versions such as `v2.1`.
They have the form `vNUMBER.NUMBER`
They are the base branches for deployment.

Whenever a commit is created in these branches,
[travis][travis] does the following:

1. Test the branch
2. Create a new tag with increasing number.
   I.e. for the branch `v2.1` the tag `v2.1.0` is created,
   if this exists `v2.1.1` and so on.
   This tag is pushed to github.

Whenever a tag is built with [travis][travis], the following is checked:

1. Does the tag correspond to the `__version__` variable on the module?
2. If yes, the current build is pushed to [pypi][pypi].

Test
----

```sh
python hanging_threads.py
```

Manual Upload
-------------

To install wheel:

```sh
pip install wheel
```

Upload Linux:

```
python setup.py bdist bdist_wheel sdist upload
```

Upload Windows:

```
py -3.4 setup.py bdist_wheel sdist upload
```

[travis]: https://github.com/niccokunzmann/hanging_threads
[pypi]: https://pypi.python.org/pypi/hanging_threads
