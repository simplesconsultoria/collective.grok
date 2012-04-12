# -*- coding:utf-8 -*-
from collective.grok import gs
from Products.GenericSetup.interfaces import EXTENSION

gs.profile(name=u'testing',
           title=u'A fake profile',
           description=u'A fake profile for ZCMLess config',
           directory='profiles/testing',
           provides=EXTENSION)
