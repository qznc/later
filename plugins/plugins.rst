Later Plugins
=============

Plugins for the *later* issue tracker are just .py files,
which are put into the ``.later`` data directory.
They contain a ``plugin_init`` function,
which is called to start the plugin.
A plugin can change the hooks.

Example
-------

If you use *later* within a git repository,
copy the ``git.py`` plugin into your ``.later``
and *later* will use the git info to guess the reporter.

