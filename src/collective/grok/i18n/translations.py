# -*- coding:utf-8 -*-
import os
import sys


def registerTranslations(directory=None):
    ''' Register an i18n directory '''
    frame = sys._getframe(1)
    try:
        file_path = frame.f_locals['__file__']
    except KeyError:
        # Called from a function?
        file_path = frame.f_globals['__file__']
    base_path = os.path.dirname(file_path)
    if directory is None:
        directory = 'locales'
    directory = os.path.join(base_path, directory)
    # XXX we do not have function grokkers (yet) so we put the annotation
    # on the module and defer its registration.
    i18n_translations = frame.f_locals.get('__grok_i18n_translations__', None)
    if i18n_translations is None:
        frame.f_locals['__grok_i18n_translations__'] = i18n_translations = []

    i18n_translations.append(directory)
