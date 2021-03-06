**************************************
Content Rules: Set layout
**************************************

.. contents:: Content
   :depth: 2

Overview
--------

**Content Rules: Set Layout** (sc.contentrules.layout) package provides
a content rule action to set a layout or default view for a content item.

Use case
---------

Some Plone content types allows the user to select one of many available layouts
to be used as default view. A good example is the Folder content type which
provides options like Folder Summary View and Tabular View.

It is possible to change the default view for a content type but it will affect
the entire portal, so if an editor wants to, in an area of the portal, to change
the default view of newly created Folder content items to Folder Summary View,
he will need to do it manually.

This package provides an action, **Set Layout** that allows content managers
, using content rules, to selectively apply layouts to content items.


Actions
---------

This package provides a content rule action to set the layout (default view) for
a content object.

Set layout
^^^^^^^^^^^^^^^^^^^

Used to create a new user group this action have three options:

Layout
    A layout to be applied to the content item that triggered the content rule.
    This action will inspect the content rule conditions and look for a
    **Content Type condition** to select the available layouts. If no condition
    is found the only available value in here will be Default View. Also, if
    there is a **Content Type condition** but two or more content types are
    selected, this action will provide you with an intersection of available
    views for all selected content types


Installation
------------

Include this package in eggs and zcml section of your buildout. For further reference please refer to the `official guide`_.

Requirements
------------

    * Plone 4.2.x and above (http://plone.org/products/plone)

Mostly Harmless
---------------

.. image:: https://secure.travis-ci.org/simplesconsultoria/sc.contentrules.layout.png
    :target: http://travis-ci.org/simplesconsultoria/sc.contentrules.layout

.. image:: https://coveralls.io/repos/simplesconsultoria/sc.contentrules.layout/badge.png :target: https://coveralls.io/r/simplesconsultoria/sc.contentrules.layout

Have an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`opening a support ticket`: https://github.com/simplesconsultoria/sc.contentrules.layout/issues

.. _`official guide`: http://plone.org/documentation/manual/developer-manual/managing-projects-with-buildout/installing-a-third-party-product
