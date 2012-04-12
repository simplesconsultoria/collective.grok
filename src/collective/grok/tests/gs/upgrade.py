# -*- coding:utf-8 -*-
from collective.grok import gs


@gs.upgradestep(title='Fake Upgrade', description='Change the portal title',
                source='0.0', destination='1000', sortkey=1,
                profile='collective.grok:fake')
def my_upgrade_step(context):
    from Products.CMFCore.utils import getToolByName
    portal = getToolByName(context, 'portal_url').getPortalObject()
    portal.title = 'Changed Title'
