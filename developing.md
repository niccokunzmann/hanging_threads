Notes on Development
====================

How to contribute
-----------------

You can contribute to the latest version and fix bugs in old versions.

Latest Version
~~~~~~~~~~~~~~

This works as usually: You can create a pull-request to the master branch.
As soon as the master branch gets merged into the latest deploy branch,
your fix will be [live][pypi].
Deploy branches are named like versions. Example: `v2.0`.

Old Versions
~~~~~~~~~~~~
Mostly, you would like to contribute to the latest version and the master
branch.
If you really think that a fix is required to on old version of the software,
you can do this.

The deploy process works like this for old versions:

Create a pull-request to the branch of the old version:

1. Check which [release][pypi] has the bug. (Example: 2.0.0)
2. Have a look at the tag (Example: v2.0.0)
   and the corresponding branch (Example: v2.0).
3. Choose the branch as the basis of your pull-request. Example:
   ```sh
   git checkout v2.0
   git checkout -b my-pull-request-branch
   ```
4. Send a pull request to the branch.
5. It gets merged and a new release is issued.
6. We may want to create more pull-requests from this branch
   to other release branches to add the feature there, too.


Deployment
----------

### Short

Merge [`master` into `v2.0`](https://github.com/niccokunzmann/hanging_threads/compare/v2.0...master).

```sh
git checkout v2.0
git pull
./create-tag-on-deploy-branch.sh origin
```

### Long

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
