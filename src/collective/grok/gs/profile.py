# -*- coding:utf-8 -*-
import sys

from Products.GenericSetup.interfaces import BASE


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

    # XXX we do not have function grokkers (yet) so we put the annotation
    # on the module and defer its registration.
    gs_profiles = frame.f_locals.get('__grok_profiles__', None)
    if gs_profiles is None:
        frame.f_locals['__grok_profiles__'] = gs_profiles = []

    profile = (name, title, description, directory, product, provides, for_)
    gs_profiles.append(profile)
