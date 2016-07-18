===========
pyspotlight
===========

is a thin python wrapper around `DBpedia Spotlight`_'s `REST Interface`_.

The tested DBpedia Spotlight versions are 0.5 and 0.6.5, though it seems to also work with 0.7 as confirmed by some users.
As long as there are no major API overhauls, this wrapper might also
work with future versions. If you encounter a bug with a newer DBpedia version,
feel free to create an issue here on github.

Note that we're trying to track DBpedia Spotlight release version numbers, so you can
easily see which pyspotlight version has been tested with which Spotlight
release. Therefore all pyspotlight 0.5 releases are tested against
Spotlight 0.5 etc.

.. _`DBpedia Spotlight`: https://github.com/dbpedia-spotlight/dbpedia-spotlight#dbpedia-spotlight
.. _`REST Interface`: https://github.com/dbpedia-spotlight/dbpedia-spotlight/wiki/Web-service

Installation
============

The newest stable release can be found on the `Python Package Index (PyPi) <https://pypi.python.org/pypi>`__.

Therefore installation is as easy as::

    pip install pyspotlight

Requirements for installation from source/github
================================================

This module has been tested with Python 2.7 and Python 3.5.

As long as you use the ``setup.py`` for the installation
(``python setup.py install``), you'll be fine because Python takes care of the
dependencies for you.

If you decide not to use the ``setup.py`` you will need the ``requests``
library. In case you are running a Python Version older than 2.7, you will
also need to install the ``ordereddict`` module.

All of these packages can be found on the `Python PackageIndex`_ and easily
installed via either ``easy_install`` or, `the recommended`_, ``pip``.

Using ``pip`` it is especially easy because you can just do this::

    pip install -r requirements.txt

and it will install all packages from that file.

.. _`Python PackageIndex`: http://pypi.python.org/
.. _`the recommended`: http://stackoverflow.com/questions/3220404/why-use-pip-over-easy-install

Usage
=====

if you just want to play around with spotlight, there is a running version
available under ``http://spotlight.sztaki.hu:LANG_PORT/rest/annotate``, where ``LANG_PORT`` is one of the following depending on the language you want to annotate (thx to @robert-boulanger in Issue #10)::

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

(Also the public server doesn't like the ``LingPipeSpotter``, which is used by *pyspotlight* by default. To work around this, simply pass ``spotter='Default'`` to the ``annotate()`` call)

Usage is simple and easy, just as is the API::

    >>> import spotlight
    >>> annotations = spotlight.annotate('http://localhost/rest/annotate',
    ...                                  'Your test text',
    ...                                  confidence=0.4, support=20)

This should return a list of all resources found within the given text.
Assuming we did this for the following text::

    President Obama on Monday will call for a new minimum tax rate for individuals making more than $1 million a year to ensure that they pay at least the same percentage of their earnings as other taxpayers, according to administration officials.

We might get this back::

    >>> annotation
    [{u'URI': u'http://dbpedia.org/resource/Presidency_of_Barack_Obama',
      u'offset': 0,
      u'percentageOfSecondRank': -1.0,
      u'similarityScore': 0.10031112283468246,
      u'support': 134,
      u'surfaceForm': u'President Obama',
      u'types': u'DBpedia:OfficeHolder,DBpedia:Person,Schema:Person,Freebase:/book/book_subject,Freebase:/book,Freebase:/book/periodical_subject,Freebase:/media_common/quotation_subject,Freebase:/media_common'},…(truncated remaining elements)…]

The same parameters apply to the ``spotlight.candidates`` function.

The following exceptions can occur:

* ``ValueError`` when:

  - the JSON response could not be decoded.

* ``SpotlightException`` when:

  - the JSON response did not contain any needed fields or was not formed as
    excepted.
  - You forgot to explicitly specify a protocol (http/https) in the API URL.

  Usually the exception's message is telling you *exactly* what is wrong. If
  not, I might have forgotten some error handling. So just open up an issue on
  github.

* ``requests.exceptions.HTTPError``

  Is thrown when the response http status code was *not* ``200``. This could happen
  if you have a load balancer like nginx in front of your spotlight cluster and
  there is not a single server available, so nginx throws a ``502 Bad Gateway``.


Note that the API also supports a ``disambiguate`` interface, however I wasn't
able to get it running. Therefore there is *no* ``disambiguate`` function
available. Feel free to contribute :-)!

Tips
====

I'd highly recommend playing around with the *confidence* and *support* values.
Furthermore it might be preferable to filter out more annotations by looking
at their *smiliarityScore* (read: contextual score).

If you want to change the default values, feel free to use ``itertools.partial``
to create a little wrapper with simplified signature::

    >>> from spotlight import annotate
    >>> from functools import partial
    >>> api = partial(annotate, 'http://localhost/rest/annotate',
    ...               confidence=0.4, support=20,
    ...               spotter='AtLeastOneNounSelector')
    >>> api('This is your test text. This function has other confidence,
    ...      support and uses another spotter. Furthermore all calls go
    ...      directl to localhost/rest/annotate.')

As you can see this reduces the function's complexity greatly.
I did not feel the need to create fancy classes, they would've just lead to
more complexity.

Tests
=====

If you want to run the tests, you will have to install ``nose`` (1.2.1) from the
package index. Then you can simply run ``nosetests`` from the command line in
this or the ``spotlight/`` directory.

Bugs
====

In case you spot a bug, please open an issue and attach the raw response you
sent. Have a look at `Issue #3`_ for a great example on how to file a bug report.

.. _`Issue #3`: https://github.com/newsgrape/pyspotlight/issues/3
