# -*- coding:utf-8 -*-
from collective.grok import gs


@gs.importstep(name=u'fake-import-step', title='Fake Import Step',
               description='Change the portal title', dependencies=[])
def my_import_step(context):
    from Products.CMFCore.utils import getToolByName
    portal = getToolByName(context, 'portal_url').getPortalObject()
    portal.title = 'Import Step Title'
