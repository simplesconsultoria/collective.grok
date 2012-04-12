# -*- coding:utf-8 -*-
import sys
from Products.GenericSetup.interfaces import BASE
from Products.GenericSetup.registry import _profile_registry


def profile(name=u'default', title=None, description=None,
            directory='', provides=BASE, for_=None):
    ''' Register a profile for GenericSetup '''
    frame = sys._getframe(1)
    try:
        product = frame.f_locals['__package__']
    except KeyError:
        # Called from a function?
        product = frame.f_globals['__package__']
    if directory is None:
        directory = 'profiles/%s' % name

    if title is None:
        title = u"Profile '%s' from '%s'" % (name, product)

    if description is None:
        description = u''

    _profile_registry.registerProfile(name,
                                      title,
                                      description,
                                      directory,
                                      product,
                                      provides,
                                      for_)
