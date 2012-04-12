# -*- coding:utf-8 -*-
import martian

from zope.i18n.zcml import registerTranslations

from Products.GenericSetup.registry import _export_step_registry
from Products.GenericSetup.registry import _import_step_registry
from Products.GenericSetup.registry import _profile_registry
from Products.GenericSetup.upgrade import _registerUpgradeStep

from Products.GenericSetup.upgrade import UpgradeStep


# Generic Setup
class ProfileGrokker(martian.GlobalGrokker):

    def grok(self, name, module, module_info, config, **kw):
        gs_profiles = module_info.getAnnotation('grok.profiles', [])
        for profile in gs_profiles:
            _profile_registry.registerProfile(*profile)
        return True


class ExportStepDecoratorGrokker(martian.GlobalGrokker):

    def grok(self, name, module, module_info, config, **kw):
        gs_steps = module_info.getAnnotation('grok.exportsteps', [])
        for step in gs_steps:
            _export_step_registry.registerStep(step.get('name'),
                                               step.get('function'),
                                               step.get('title'),
                                               step.get('description'))
        return True


class ImportStepDecoratorGrokker(martian.GlobalGrokker):

    def grok(self, name, module, module_info, config, **kw):
        gs_steps = module_info.getAnnotation('grok.importsteps', [])
        for step in gs_steps:
            _import_step_registry.registerStep(step.get('name'),
                                               None,
                                               step.get('function'),
                                               step.get('dependencies'),
                                               step.get('title'),
                                               step.get('description'))
        return True


class UpgradeStepDecoratorGrokker(martian.GlobalGrokker):

    def grok(self, name, module, module_info, config, **kw):
        gs_steps = module_info.getAnnotation('grok.upgradesteps', [])
        for step in gs_steps:
            step = UpgradeStep(step.get('title'),
                               step.get('profile'),
                               step.get('source'),
                               step.get('destination'),
                               step.get('description'),
                               step.get('function'),
                               None,
                               step.get('sortkey'))
            # Do the actual registration
            _registerUpgradeStep(step)
        return True


# i18n
class RegisterTranslationsGrokker(martian.GlobalGrokker):

    def grok(self, name, module, module_info, config, **kw):
        i18n_translations = module_info.getAnnotation('grok.i18n.translations',
                                                      [])
        for t_directory in i18n_translations:
            registerTranslations(config, t_directory)
        return True
