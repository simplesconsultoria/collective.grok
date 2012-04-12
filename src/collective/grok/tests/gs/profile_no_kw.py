# -*- coding:utf-8 -*-
from collective.grok import gs
from Products.GenericSetup.interfaces import EXTENSION

gs.profile(u'testing_no_kw',
           u'A fake profile',
           u'A fake profile for ZCMLess config',
           'profiles/testing',
           EXTENSION)
