===========
pyspotlight
===========

is a thin python wrapper around `DBpedia Spotlight`_'s `REST Interface`_.

This package is tested against DBpedia Spotlight version 0.7.
As long as there are no major API overhauls, this wrapper might also
work with future versions. If you encounter a bug with a newer DBpedia Spotlight version,
feel free to create an issue here on github.

Note that we're trying to track DBpedia Spotlight release version numbers, so you can
easily see which pyspotlight version has been tested with which Spotlight
release. For example, all pyspotlight 0.6.x releases are compatible with
Spotlight 0.6.x, etc. While we aim for backwards-compatibility with older
Spotlight releases, it is not guaranteed. If you're using an older Spotlight
version, you may need to use an older pyspotlight version as well.

.. _`DBpedia Spotlight`: https://github.com/dbpedia-spotlight/dbpedia-spotlight#dbpedia-spotlight
.. _`REST Interface`: https://github.com/dbpedia-spotlight/dbpedia-spotlight/wiki/Web-service

Installation
============

The newest stable release can be found on the `Python Package Index (PyPI) <https://pypi.python.org/pypi>`__.

Therefore installation is as easy as::

    pip install pyspotlight

Older releases can be installed by specifying a version::

    pip install pyspotlight~=0.6

Requirements for installation from source/github
================================================

This module has been tested with Python 2.7 and Python 3.5.

As long as you use the ``setup.py`` for the installation
(``python setup.py install``), you'll be fine because Python takes care of the
dependencies for you.

If you decide not to use the ``setup.py`` you will need the ``requests``
library.

All of these packages can be found on the `Python PackageIndex`_ and easily
installed via either ``easy_install`` or, `the recommended`_, ``pip``.

Using ``pip`` it is especially easy because you can just do this::

    pip install -r requirements.txt

and it will install all package dependencies listed in that file.

.. _`Python PackageIndex`: http://pypi.python.org/
.. _`the recommended`: http://stackoverflow.com/questions/3220404/why-use-pip-over-easy-install

Usage
=====

Usage is simple and easy, just as the API is::

    >>> import spotlight
    >>> annotations = spotlight.annotate('http://localhost/rest/annotate',
    ...                                  'Your test text',
    ...                                  confidence=0.4, support=20)

This should return a list of all resources found within the given text.
Assuming we did this for the following text::

    President Obama on Monday will call for a new minimum tax rate for individuals making more than $1 million a year to ensure that they pay at least the same percentage of their earnings as other taxpayers, according to administration officials.

We might get this back::

    >>> spotlight.annotate('http://localhost/rest/annotate', sample_txt)
    [
      {
        'URI': 'http://dbpedia.org/resource/Presidency_of_Barack_Obama',
        'offset': 0,
        'percentageOfSecondRank': -1.0,
        'similarityScore': 0.10031112283468246,
        'support': 134,
        'surfaceForm': 'President Obama',
        'types': 'DBpedia:OfficeHolder,DBpedia:Person,Schema:Person,Freebase:/book/book_subject,Freebase:/book,Freebase:/book/periodical_subject,Freebase:/media_common/quotation_subject,Freebase:/media_common'
      },
      …(truncated remaining elements)…
    ]

Any additional filter parameters that are supported by the Spotlight API
can be passed to the ``filters`` argument in a dictionary.

For example::

    >>> only_person_filter = {
    ...     'policy': "whitelist",
    ...     'types': "DBpedia:Person",
    ...     'coreferenceResolution': False
    ... }

    >>> spotlight.annotate(
    ...     "http://localhost/rest/annotate",
    ...     "Any collaboration between Shakira and Metallica seems highly unlikely.",
    ...     filters=only_person_filter
    ... )

    [{
        'URI': 'http://dbpedia.org/resource/Shakira',
        'offset': 26,
        'percentageOfSecondRank': 1.511934771738109e-09,
        'similarityScore': 0.9999999984880361,
        'support': 2587,
        'surfaceForm': 'Shakira',
        'types': 'Schema:MusicGroup,DBpedia:Agent,Schema:Person,DBpedia:Person,DBpedia:Artist,DBpedia:MusicalArtist'
    }]

The same parameters apply to the ``spotlight.candidates`` function,
which returns a list of all matching candidate entities rather than
only the top candidate.

Note that the Spotlight API may support other interfaces that have not been
implemented in pyspotlight. Feel free to contribute :-)!

DBpedia Spotlight demo server
-----------------------------
If you just want to play around with spotlight, there is a running version
available under ``http://spotlight.sztaki.hu:LANG_PORT/rest/annotate``, where ``LANG_PORT`` is one of the following depending on the language you want to annotate (thanks @robert-boulanger in `ubergrape/pyspotlight#10`_)::

    LANG_PORTS = {
        "english": '2222',
        "german": '2226',
        "dutch": '2232',
        "hungarian": '2229',
        "french": '2225',
        "portuguese": '2228',
        "italian": '2230',
        "russian": '2227',
        "turkish": '2235',
        "spanish": '2231'
    }

.. _`ubergrape/pyspotlight#10`: https://github.com/ubergrape/pyspotlight/issues/10

Exceptions
----------
The following exceptions can occur:

* ``ValueError`` when:

  - the JSON response could not be decoded.

* ``SpotlightException`` when:

  - the JSON response did not contain any needed fields or was not formed as
    excepted.
  - You forgot to explicitly specify a protocol (http/https) in the API URL.

  Usually the exception's message tells you *exactly* what is wrong. If
  not, we might have forgotten some error handling. So just open up an issue on
  github if you encounter unexpected exceptions.

* ``requests.exceptions.HTTPError``

  Is thrown when the response http status code was *not* ``200``. This could happen
  if you have a load balancer like nginx in front of your spotlight cluster and
  there is not a single server available, so nginx throws a ``502 Bad Gateway``.

Tips
====

We highly recommend playing around with the *confidence* and *support* values.
Furthermore it might be preferable to filter out more annotations by looking
at their *similiarityScore* (read: contextual score).

If you want to change the default values, feel free to use ``itertools.partial``
to create a little wrapper with simplified signature::

    >>> from spotlight import annotate
    >>> from functools import partial
    >>> api = partial(annotate, 'http://localhost/rest/annotate',
    ...               confidence=0.4, support=20,
    ...               spotter='SpotXmlParser')
    >>> api('This is your test text. This function uses a non-default
    ...      confidence, support, and spotter. Furthermore all calls go
    ...      directly to localhost/rest/annotate.')

As you can see this reduces the function's complexity greatly.
Pyspotlight provides an interface based on functions rather than classes,
to avoid an unnecessary layer of indirection.

Tests
=====

If you want to run the tests, you will have to install ``nose2`` (~0.6) from PyPI.
Then you can simply run ``nose2`` from the command line in
this or the ``spotlight/`` directory.

All development and regular dependencies can be installed with a single command::

    pip install -r requirements-dev.txt


Bugs
====

In case you spot a bug, please open an issue and attach the raw response you
sent. Have a look at `ubergrape/pyspotlight#3`_ for an example on how to file a good bug report.

.. _`ubergrape/pyspotlight#3`: https://github.com/ubergrape/pyspotlight/issues/3
