Notes on Development
====================

Test:
----

```sh
python hanging_threads.py
```

Upload
------

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
