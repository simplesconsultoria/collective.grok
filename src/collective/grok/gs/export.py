# -*- coding:utf-8 -*-
import sys


class exportstep:

    def __init__(self, name, title, description):
        self.name = name
        self.title = title
        self.description = description

    def __call__(self, ob):
        # XXX we do not have function grokkers (yet) so we put the annotation
        # on the module.
        frame = sys._getframe(1)
        gs_steps = frame.f_locals.get('__grok_exportsteps__', None)
        if gs_steps is None:
            frame.f_locals['__grok_exportsteps__'] = gs_steps = []
        step = dict(name=self.name,
                    title=self.title,
                    description=self.description,
                    function=ob)
        gs_steps.append(step)
        return ob
