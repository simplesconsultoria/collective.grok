# -*- coding: utf-8 -*-
import os
import unittest2 as unittest

import grokcore.component.testing

from zope.site.hooks import setSite
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

from zope.i18n.interfaces import ITranslationDomain

from collective.grok.tests import i18n

from collective.grok.testing import INTEGRATION_TESTING

PROJECTNAME = 'collective.grok'


class BaseTestCase(unittest.TestCase):
    """base test case to be used by other tests"""

    layer = INTEGRATION_TESTING

    def setUpUser(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor', 'Reviewer'])
        login(self.portal, TEST_USER_NAME)

    def setUp(self):
        portal = self.layer['portal']
        setSite(portal)
        self.portal = portal
        self.st = getattr(self.portal, 'portal_setup')
        self.base_path = os.path.dirname(i18n.__file__)
        self.setUpUser()


class TestRegisterTranslations(BaseTestCase):
    """ Test Locales Folder registration """

    def test_not_registered(self):
        util = queryUtility(ITranslationDomain, 'collective.grok.tests.i18n')
        self.assertTrue(util == None)

    def test_registered(self):
        path = os.path.join(self.base_path, 'locales', 'es', 'LC_MESSAGES',
                            'collective.grok.tests.i18n.mo')
        # Register translations
        gs_module = 'collective.grok.tests.i18n.translations'
        grokcore.component.testing.grok(gs_module)
        util = queryUtility(ITranslationDomain, 'collective.grok.tests.i18n')
        self.assertEquals(util._catalogs.get('es'),
                          [unicode(path)])


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
