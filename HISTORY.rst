Changelog
=========

v0.7.1 (2016-07-25)
-------------------

- Moved the shared request logic in ``annotate`` and ``candidates`` to a
  helper function.
  [Alex Olieman]

- Updated setup/package files [Alex Olieman]

- Updated README. [Luis Nell & Alex Olieman]

v0.7.0 (2016-07-18)
-------------------

API Changes
~~~~~~~~~~~

- Changed default spotter to ``'Default'`` for 0.7 compatibility. [Alex
  Olieman]

- Moved filter parameters into a ``filters`` argument. [Alex Olieman]

  * **Removed** the ``policy`` argument from ``annotate()`` and ``candidates()``.
  * Added a types parameter, which enables server-side filtering of resources.
    It also makes for a nice addition to the policy parameter.

Additions
~~~~~~~~~

- Py3-compatible 0.7 release. [Alex Olieman]

- Moved to nose2 for tests. [Alex Olieman]

Fixes
~~~~~

- Updated required version of the requests package. [Alex Olieman]

- Remove dict from method signature. fixes #8. [Luis Nell]

v0.6.5.2 (2013-08-27)
---------------------

- Add manifest so README is included on pypi. [Luis Nell]

v0.6.5.1 (2013-08-12)
---------------------

- Update README for pypi release. [Luis Nell]

- Upgrade to requests 1.2.3. [Luis Nell]

- BSD License. [Luis Nell]

- Workaround footnotes in surfaceForm parsed as list. fixes #4. [Luis
  Nell]

- Fix #3. [Luis Nell]

v0.6.5 (2012-10-07)
-------------------

API Changes
~~~~~~~~~~~

- Have to explicitly provide a protocol in the URL. [Luis Nell]

Additions
~~~~~~~~~

- Added stuff for testing. [Luis Nell]

- Add requirements.txt for pip. [Luis Nell]

- Make use of requests builtin json decoding. [Luis Nell]

Fixes
~~~~~

- Some README updates. [Luis Nell]

- Add ordereddict requirement for py2.6. [Luis Nell]

- Tests: adapt to the requests raw handling. [Luis Nell]

- Use requests 0.14.1 from now on. [Luis Nell]

- Fixed typos, wrong link. [Pablo Mendes]

  * Minor: We spell it DBpedia, not DBPedia :)
  * Fix: Link pointed to OpenCalais, a commercial closed-source alternative to DBpedia Spotlight

v0.5.3 (2012-08-01)
-------------------

- Update README to reflect the exception changes. [Luis Nell]

- Raise requests.exceptions.HTTPError on response.status_code != 200.
  [Luis Nell]

- Prefer simplejson to json. [Luis Nell]

- Add tests for new exception handling. [Luis Nell]

- Add Exception Handling. [Luis Nell]

v0.5.2 (2012-04-06)
-------------------

- Fixes setup.py issues. v0.5.2. [Luis Nell]

v0.5.1 (2012-03-21)
-------------------

- Fix setup.py - push 0.5.1. [Luis Nell]

v0.5.0 (2012-03-20)
-------------------

- Init. [Luis Nell]
