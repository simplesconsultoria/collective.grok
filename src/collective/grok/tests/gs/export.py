# -*- coding:utf-8 -*-
from collective.grok import gs


@gs.exportstep(name=u'fake-export-step', title='Fake Export Step',
               description='Change the portal title')
def my_export_step(context):
    from Products.CMFCore.utils import getToolByName
    portal = getToolByName(context, 'portal_url').getPortalObject()
    portal.title = 'Export Step Title'
