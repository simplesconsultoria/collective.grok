# -*- coding:utf-8 -*-
import sys


class importstep:

    def __init__(self, name, title, description='', dependencies=[]):
        self.name = name
        self.title = title
        self.description = description
        self.dependencies = dependencies

    def __call__(self, ob):
        # XXX we do not have function grokkers (yet) so we put the annotation
        # on the module.
        frame = sys._getframe(1)
        gs_steps = frame.f_locals.get('__grok_importsteps__', None)
        if gs_steps is None:
            frame.f_locals['__grok_importsteps__'] = gs_steps = []
        step = dict(name=self.name,
                    title=self.title,
                    description=self.description,
                    dependencies=self.dependencies,
                    function=ob)
        gs_steps.append(step)
        return ob
