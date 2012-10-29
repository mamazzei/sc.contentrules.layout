# -*- coding:utf-8 -*-

import unittest2 as unittest

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from zope.interface import implements
from zope.component import getUtility
from zope.component import getMultiAdapter

from zope.component.interfaces import IObjectEvent

from zope.schema.interfaces import IVocabularyFactory

from plone.app.contentrules.rule import Rule

from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IRuleAction
from plone.contentrules.rule.interfaces import IRuleCondition
from plone.contentrules.rule.interfaces import IExecutable

from sc.contentrules.layout.config import VOCAB

from sc.contentrules.layout.actions.layout import SetLayoutAction
from sc.contentrules.layout.actions.layout import SetLayoutEditForm

from sc.contentrules.layout.testing import INTEGRATION_TESTING


class DummyEvent(object):
    implements(IObjectEvent)

    def __init__(self, object):
        self.object = object


class TestSetLayoutAction(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'folder')
        self.folder = self.portal['folder']
        sub_folder_id = self.folder.invokeFactory('Folder', 'sub_folder')
        self.sub_folder = self.folder[sub_folder_id]

    def testRegistered(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.layout')
        self.assertEquals('sc.contentrules.actions.layout',
                          element.addview)
        self.assertEquals('edit', element.editview)
        self.assertEquals(None, element.for_)
        self.assertEquals(IObjectEvent, element.event)

    def testInvokeAddView(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.layout')
        storage = getUtility(IRuleStorage)
        storage[u'foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')

        adding = getMultiAdapter((rule, self.portal.REQUEST),
                                 name='+action')
        addview = getMultiAdapter((adding, self.portal.REQUEST),
                                  name=element.addview)

        addview.createAndAdd(data={'layout': 'folder_summary_view'})

        e = rule.actions[0]
        self.failUnless(isinstance(e, SetLayoutAction))
        self.assertEquals('folder_summary_view', e.layout)

    def testInvokeEditView(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.layout')
        e = SetLayoutAction()
        editview = getMultiAdapter((e, self.folder.REQUEST),
                                   name=element.editview)
        self.failUnless(isinstance(editview, SetLayoutEditForm))

    def testExecute(self):
        e = SetLayoutAction()
        e.layout = 'folder_summary_view'

        ex = getMultiAdapter((self.folder, e,
                             DummyEvent(self.sub_folder)),
                             IExecutable)
        self.assertEquals(True, ex())

        self.assertEquals(self.sub_folder.layout, e.layout)

    def testExecuteWithError(self):
        e = SetLayoutAction()
        e.layout = 'document_view'

        ex = getMultiAdapter((self.folder, e,
                             DummyEvent(self.sub_folder)),
                             IExecutable)
        self.assertEquals(False, ex())
        # Layout not set
        self.assertEquals(hasattr(self.sub_folder, 'layout'), False)


class TestActionWithCondition(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'folder')
        self.folder = self.portal['folder']
        sub_folder_id = self.folder.invokeFactory('Folder', 'sub_folder')
        self.sub_folder = self.folder[sub_folder_id]


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
