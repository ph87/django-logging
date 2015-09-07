#summary Information about the profiling branch
#labels Featured

# Introduction #

This page describes the **profiling** branch for _django-logging_. This introduces
additional functionality to make use of the Python's
[profiling capabilities](http://docs.python.org/lib/profile.html).

# Installation #

The branch can be checked out from:

```
svn co http://django-logging.googlecode.com/svn/branches/profiling/djangologging/ djangologging
```

The basic installation instructions are the same as those on the [Overview](Overview.md)
page. The new `LOGGING_PROFILER` setting must also be provided to enable
profiling:

| **Variable**         | **Default** | **Description** |
|:---------------------|:------------|:----------------|
| `LOGGING_PROFILER`   | `None`      | To enable profiling, set this to a supported profiler. Currently this can be either `hotshot` or `cProfile`. |

# Todo #

  * Store the profile data in a FIFO queue so that only data from the last _n_ requests is kept.
  * Make the graph thumbnail draggable for fast panning.
  * Allow sorting, grouping, etc. on the raw statistics.
  * Add `trans` and `blocktrans` tags to the new templates.

# Feedback #

This branch is effectively a beta pre-release, so I'm keen to get feedback and
ideas for what it should do. If you spot any bugs or want to make a suggestion,
please use the
[issue tracker](http://code.google.com/p/django-logging/issues/list), or
[contact me directly](http://www.nevett.org/contact).

Thanks,

Fraser