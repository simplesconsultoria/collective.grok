collective.grok
**************************************************************

.. contents:: Table of Contents
   :depth: 2


Overview
===========

**collective.grok** intends to reduce the need for ZCML usage in Plone
projects.

Using the infrastructure provided by 
`five.grok <http://pypi.python.org/pypi/five.grok>`_ and 
`martian <http://pypi.python.org/pypi/martian>`_, this package
adds new decorators and helper functions to enable Plone developers ...

Installation
=============

This package is intended to be a dependency of other packages, so declare
it on the **setup.py** of your package, under *install_requires*:
::
    
        install_requires=[
        'setuptools',
        # XXX: Add extra requirements here
        'collective.grok',
        ],


.. note:: There is no need to explicitly declare *five.grok* as
          *collective.grok* already does that.

Usage
===========

In order to make it *fit your mind* to collective.grok groups its helpers
in packages according to Plone technologies it addresses, for example,
*collective.grok.gs* deals with Generic Setup.


Generic Setup
---------------

The most commonly used Generic Setup registrations implemented by ZCML are supported in the current release of collective.grok.

Registering Profiles
^^^^^^^^^^^^^^^^^^^^^^^^^

To register a profile with ZCML you should add the following element to 
configure.zcml (or some other file included by it). 

::

      <genericsetup:registerProfile
        name="default"
        title="Portal policy for plone.org"
        directory="profiles/default"
        description="Installs dependencies and stuff for our portal"
        provides="Products.GenericSetup.interfaces.EXTENSION"
        i18n:attributes="title; description"
        />


Using collective.grok, the same registration would be done (verbosily):

::
    
    from collective.grok import gs
    from Products.GenericSetup.interfaces import EXTENSION
    gs.profile(name=u'default',
               title=u'Portal policy for plone.org',
               description=u'Installs dependencies and stuff for our portal',
               directory='profiles/default',
               provides=EXTENSION)


To register a second profile (in our case, one for uninstall), we would
do the same (now, without passing the parameter names):

::

    gs.profile(u'uninstall',
               u'Uninstall portal policy for plone.org',
               u'Removes dependencies and stuff from our portal',
               'profiles/uninstall',
               EXTENSION)

And i18n is supported using zope.i18nmessageid MessageFactory. In the
following profile registration, we translate the profile title and
its description:

::
    
    from my.package import MessageFactory as _
    gs.profile(u'init',
               _(u'Initial content structure for plone.org'),
               _(u'Constructs folder structure and navigation'),
               'profiles/init',
               EXTENSION)



Registering Export Steps
^^^^^^^^^^^^^^^^^^^^^^^^^

Using ZCML to register an export step for Generic Setup demanded the
inclusion of the following element element to configure.zcml (or some other file included by it). 

::

    <genericsetup:exportStep
        name="archetypetool"
        title="Archetype Tool"
        description="Export Archetype Tool."
        handler="Products.Archetypes.exportimport.archetypetool.exportArchetypeTool">
    </genericsetup:exportStep>


The registration points to a handler, which implements the actual export
code:

::

    def exportArchetypeTool(context):
        """Export Archetype Tool configuration.
        """
        site = context.getSite()
        logger = context.getLogger("archetypetool")
        tool = getToolByName(site, TOOL_NAME, None)
        if tool is None:
          return

        exportObjects(tool, '', context)
        logger.info("Archetype tool exported.")



Grokking it, the same registration would be done on the
archetypetool module with an import and a decorator:

::
    
    from collective.grok import gs
    
    @gs.exportstep(name=u'archetypetool', title='Archetype Tool',
                   description='Export Archetype Tool.')
    def exportArchetypeTool(context):
        """Export Archetype Tool configuration.
        """
        site = context.getSite()
        logger = context.getLogger("archetypetool")
        tool = getToolByName(site, TOOL_NAME, None)
        if tool is None:
          return

        exportObjects(tool, '', context)
        logger.info("Archetype tool exported.")


Again, you could even omit parameter names if you want...

::
    
    from collective.grok import gs
    
    @gs.exportstep(u'archetypetool','Archetype Tool',
                   'Export Archetype Tool.')
    def exportArchetypeTool(context):
        """Export Archetype Tool configuration.
        """
        site = context.getSite()
        logger = context.getLogger("archetypetool")
        tool = getToolByName(site, TOOL_NAME, None)
        if tool is None:
          return

        exportObjects(tool, '', context)
        logger.info("Archetype tool exported.")


Registering Import Steps
^^^^^^^^^^^^^^^^^^^^^^^^^

Import Steps are delt similarly to Export Steps. So, ZCML registration
is done (zcml file):

::

  <genericsetup:importStep
      name="archetypes-various"
      title="Archetypes setup"
      description="Import various settings for Archetypes."
      handler="Products.Archetypes.setuphandlers.setupArchetypes">
     <depends name="componentregistry"/>
  </genericsetup:importStep>


And respective Python Code:

::

    def setupArchetypes(context):
        """
        Setup Archetypes step.
        """
        # Only run step if a flag file is present (e.g. not an extension profile)
        if context.readDataFile('archetypes-various.txt') is None:
            return
        out = []
        site = context.getSite()
        install_uidcatalog(out, site)
        install_referenceCatalog(out, site)
        install_templates(out, site)


Grokking it, we would have:

::
    
    from collective.grok import gs
    
    @gs.importstep(name=u'archetypetool', title='Archetype Tool',
                   description='Export Archetype Tool.',
                   dependecies=['componentregistry',])
    def setupArchetypes(context):
        """
        Setup Archetypes step.
        """
        # Only run step if a flag file is present (e.g. not an extension profile)
        if context.readDataFile('archetypes-various.txt') is None:
            return
        out = []
        site = context.getSite()
        install_uidcatalog(out, site)
        install_referenceCatalog(out, site)
        install_templates(out, site)



Registering Upgrade Steps
^^^^^^^^^^^^^^^^^^^^^^^^^^

To register an upgrade step using ZCML the following slug should be added to
configure.zcml:

::

    <genericsetup:upgradeStep
        title="Update portal title"
        description="Upgrade step used to update portal title"
        source="1000"
        destination="2000"
        sortkey="1"
        handler=".to2000.from1000"
        profile="my.package:default" />


The handler code would look like:

::

    def to2000(context):
        """
        Update portal title 
        """
        site = context.getSite()
        site.title = u'A New Title'


collective.grok provide a decorator to grok this code:

::
    
    from collective.grok import gs
    
    @gs.upgradestep(title=u'Update portal title',
                    description=u'Upgrade step used to update portal title',
                    source='1000', destination='2000', sortkey=1,
                    profile='my.package:default')
    def to2000(context):
        """
        Update portal title 
        """
        site = context.getSite()
        site.title = u'A New Title'

