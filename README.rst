sow-what
========

A lightweight tool for planning vegetable gardens with a focus on
**companion planting** and **crop rotation**.


Usage
-----

To launch sow-what from the command line:

.. code:: shell

   $ make run

This builds and runs the Docker container, executes sow-what, and then exits.


Reporting issues & requesting features
--------------------------------------

If you run into bugs or want to suggest improvements, please open an issue.

When reporting a bug, it's helpful to include:

1. The versions of this package and Python you're using
2. The exact command or input you ran
3. What you expected to happen
4. What actually happened (including logs, error messages, or stack traces)


Developer Guide
---------------

Setting up your environment
...........................

We assume you have pre-commit_, pixi_, and Docker_ installed locally.
Most tasks (build, test, docs) run inside Docker for consistency.
The minimal tools you'll need outside Docker can be installed with:

.. code:: shell

   $ pixi install

Your local project directory is mounted into the container, so you can work
in your favorite editor and see changes instantly inside Docker.


Makefile shortcuts
..................

The ``Makefile`` wraps common commands. It includes shortcuts for building the
container, running tests, generating docs, and more. Run ``make`` to see the full list.


Building & running the container
................................

To build the Docker image:

.. code:: shell

   $ make build

To open an interactive shell in the container:

.. code:: shell

   $ make shell

Inside the container, you can run tests, build docs, or explore code, with your
local files mounted automatically.


Documentation
.............

We use Sphinx_ to generate documentation from both docstrings and hand-written
``.rst`` files. To build the docs:

.. code:: shell

   $ make docs

The output is written to ``docs/build/<branch-name>``, so you can keep multiple
branch builds side by side. Open ``index.html`` in your browser to view them.


Dependencies
............

Dependencies are managed with ``pyproject.toml`` and ``pixi.lock``.
See the pixi_ docs for details on updating or pinning dependencies.


Tests
.....

All tests run automatically in CI on push, but you can also run them locally
inside Docker:

.. code:: shell

   $ make test

We use pytest_ for running and reporting tests. You can also call ``pytest``
directly inside the container for finer control.


Linting
.......

Code style is enforced with ruff_ via pre-commit hooks. Hooks run automatically
on each commit, but you can also lint manually:

.. code:: shell

   $ make lint


Versioning
..........

This project follows `Semantic Versioning <https://semver.org>`_. We use
commitizen_ to bump versions across relevant files (``VERSION``,
``pyproject.toml``, ``conf.py``) and update the changelog.


Tools we use
............

- Sphinx_ — documentation engine, with numpydoc_ conventions for docstrings
- commitizen_ — automates version bumps and changelog updates
- pytest_ — Python test runner with rich logging
- pre-commit_ — manages hooks like ruff_ for linting and formatting


.. Links
.. _commitizen: https://commitizen-tools.github.io/commitizen/
.. _Docker: https://www.docker.com
.. _numpydoc: https://numpydoc.readthedocs.io/en/latest/
.. _pixi: https://pixi.sh/latest/
.. _pre-commit: https://pre-commit.com/
.. _pytest: https://pytest.org
.. _ruff: https://docs.astral.sh/ruff/formatter/
.. _Sphinx: https://www.sphinx-doc.org/en/master/index.html
