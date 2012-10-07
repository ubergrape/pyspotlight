===========
pyspotlight
===========

is a thin python wrapper around `DBpedia Spotlight`_'s `REST Interface`_.

The currently supported DBpedia Spotlight version is 0.5. However, as long as
there are no major API overhauls, this wrapper might also work with future
versions. If you encounter a bug with a newer DBpedia version, feel free to
create an issue here on github.

Note that I'm trying to track DBpedia Spotlight release version numbers, so you can
easily see which pyspotlight version has been tested with which Spotlight
release. Therefore all pyspotlight 0.5 releases are tested against
Spotlight 0.5.

.. _`DBpedia Spotlight`: https://github.com/dbpedia-spotlight/dbpedia-spotlight#dbpedia-spotlight
.. _`REST Interface`: https://github.com/dbpedia-spotlight/dbpedia-spotlight/wiki/Web-service

Requirements
============

This module has been tested with Python 2.6 and Python 2.7.

Python versions <= 2.6 need the ``simplejson`` and ``ordereddict`` modules
installed.

Furthermore you will need the awesome ``requests`` library.

As long as you use the ``setup.py`` for the installation
(``python setup.py install``), you'll be fine because Python takes care of the
dependencies for you.

Note about JSON
---------------

Python's ``json`` version sacrifices speed for portability (most stuff in
Python has to work cross-platform, so that is fine). If you see that the parsing
of JSON is a bottleneck, you might consider installing ``simplejson`` after all,
since it has C optimisations turned on.

Please note that I never, ever, had the Python 2.7+ builtin ``json`` module being
a bottleneck. I just think it could be useful for general knowledge, so I put it
here.

Usage
=====

if you just want to play around with spotlight, there is a running version
available under ``http://spotlight.dbpedia.org/rest/annotate``.

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

* ``SpotlightException`` when:

  - the response from spotlight did not contain any valid JSON.
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
