# -*- coding:utf-8 -*-
import sys


class upgradestep:

    def __init__(self, title, description, source,
                 destination, sortkey, profile):
        self.title = title
        self.description = description
        self.source = source
        self.destination = destination
        self.sortkey = sortkey
        self.profile = profile

    def __call__(self, ob):
        # XXX we do not have function grokkers (yet) so we put the annotation
        # on the module.
        frame = sys._getframe(1)
        gs_steps = frame.f_locals.get('__grok_upgradesteps__', None)
        if gs_steps is None:
            frame.f_locals['__grok_upgradesteps__'] = gs_steps = []
        step = dict(title=self.title,
                    description=self.description,
                    source=self.source,
                    destination=self.destination,
                    sortkey=self.sortkey,
                    profile=self.profile,
                    function=ob)
        gs_steps.append(step)
        return ob
