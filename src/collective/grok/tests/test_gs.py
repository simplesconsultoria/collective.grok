# -*- coding: utf-8 -*-
import unittest2 as unittest

import grokcore.component.testing

from zope.site.hooks import setSite

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

from Products.GenericSetup.upgrade import listUpgradeSteps

from collective.grok import gs

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
        self.setUpUser()


class TestUpgradeStep(BaseTestCase):
    """ Test our grokking of UpgradeStep """

    def test_not_registered(self):
        steps = listUpgradeSteps(self.st, 'collective.grok:fake', '0.0')
        self.assertFalse(len(steps), 'Upgrade step should not be registered')

    def test_registered(self):
        # Manually call grok machinery
        gs_module = 'collective.grok.tests.gs.upgrade'
        grokcore.component.testing.grok(gs_module)

        # Now we should have a upgrade step for this profile
        steps = listUpgradeSteps(self.st, 'collective.grok:fake', '0.0')
        self.assertTrue(len(steps), 'Upgrade step should be registered')

    def test_run_upgrade(self):
        gs_module = 'collective.grok.tests.gs.upgrade'
        grokcore.component.testing.grok(gs_module)
        # Get the steps
        steps = listUpgradeSteps(self.st, 'collective.grok:fake', '0.0')
        # Get the step
        oStep = steps[0].get('step')
        # Execute it
        oStep.doStep(self.st)
        self.assertTrue(self.portal.title == 'Changed Title',
                        'Upgrade step was not executed')


class TestImportStep(BaseTestCase):
    """ Test our grokking of ImportStep """

    def test_not_registered(self):
        step = self.st.getImportStep('fake-import-step')
        self.assertFalse(step is not None,
                         'Import step should not be registered')

    def test_registered(self):
        step = self.st.getImportStep('fake-import-step')
        self.assertFalse(step is not None,
                         'Import step should not be registered')
        # Register our import step
        gs_module = 'collective.grok.tests.gs.import_'
        grokcore.component.testing.grok(gs_module)

        # Now we should have a upgrade step for this profile
        step = self.st.getImportStep('fake-import-step')
        self.assertTrue(step is not None,
                        'Import step should be registered')

    def test_run_import_step(self):
        # Register our import step
        gs_module = 'collective.grok.tests.gs.import_'
        grokcore.component.testing.grok(gs_module)

        # Now we should have a upgrade step for this profile
        step = self.st.getImportStep('fake-import-step')
        step(self.st)
        self.assertTrue(self.portal.title == 'Import Step Title',
                        'Import step run as planned')


class TestExportStep(BaseTestCase):
    """ Test our grokking of ExportStep """

    def test_not_registered(self):
        step = self.st.getExportStep('fake-export-step')
        self.assertFalse(step is not None,
                         'Export step should not be registered')

    def test_registered(self):
        step = self.st.getExportStep('fake-export-step')
        self.assertFalse(step is not None,
                         'Export step should not be registered')
        # Register our import step
        gs_module = 'collective.grok.tests.gs.export'
        grokcore.component.testing.grok(gs_module)

        # Now we should have a upgrade step for this profile
        step = self.st.getExportStep('fake-export-step')
        self.assertTrue(step is not None,
                        'Export step should be registered')

    def test_run_export_step(self):
        # Register our import step
        gs_module = 'collective.grok.tests.gs.export'
        grokcore.component.testing.grok(gs_module)

        # Now we should have a upgrade step for this profile
        step = self.st.getExportStep('fake-export-step')
        step(self.st)
        self.assertTrue(self.portal.title == 'Export Step Title',
                        'Export step run as planned')


class TestProfile(BaseTestCase):
    """ Test Profile registration """

    def is_registered(self, profile_id):
        profiles = self.st.listProfileInfo()
        valid_profiles = [p for p in profiles if p.get('id') == profile_id]
        return valid_profiles and True or False

    def test_not_registered(self):
        profile_id = 'collective.grok.tests.gs:testing'
        self.assertFalse(self.is_registered(profile_id),
                         'Profile should not be registered')

    def test_registered(self):
        profile_id = 'collective.grok.tests.gs:testing'
        self.assertFalse(self.is_registered(profile_id),
                         'Profile should not be registered')
        # Register our profile
        gs_module = 'collective.grok.tests.gs.profile'
        grokcore.component.testing.grok(gs_module)

        # Now we should have a profile
        self.assertTrue(self.is_registered(profile_id),
                        'Profile should be registered')

    def test_registered_no_kw(self):
        profile_id = 'collective.grok.tests.gs:testing_no_kw'
        self.assertFalse(self.is_registered(profile_id),
                         'Profile should not be registered')
        # Register our profile
        gs_module = 'collective.grok.tests.gs.profile_no_kw'
        grokcore.component.testing.grok(gs_module)

        # Now we should have a profile
        self.assertTrue(self.is_registered(profile_id),
                        'Profile should be registered')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
