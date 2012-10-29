# -*- coding: utf-8 -*-

from OFS.SimpleItem import SimpleItem

from zope.component import adapts

from zope.interface import Interface
from zope.interface import implements

from zope.formlib import form

from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import EditForm

from plone.contentrules.rule.interfaces import IRuleElementData
from plone.contentrules.rule.interfaces import IExecutable

from Products.statusmessages.interfaces import IStatusMessage

from sc.contentrules.layout.interfaces import ISetLayoutAction
from sc.contentrules.layout.exceptions import ViewFail


from sc.contentrules.layout import MessageFactory as _


class SetLayoutAction(SimpleItem):
    """ Stores action settings
    """
    implements(ISetLayoutAction, IRuleElementData)

    element = 'sc.contentrules.actions.layout'
    layout = ''

    @property
    def summary(self):
        return _(u"Set layout ${layout} to a content item",
                 mapping=dict(layout=self.layout))


class SetLayoutActionExecutor(object):
    """ Execute an action
    """
    implements(IExecutable)
    adapts(Interface, ISetLayoutAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        '''  Apply selected layout to a content item
        '''
        context = self.context
        self._pstate = context.unrestrictedTraverse('@@plone_portal_state')
        self._ptools = context.unrestrictedTraverse('@@plone_tools')
        pt = self._ptools.types()
        layout = self.element.layout

        if layout == '_default_view':
            # Do nothing, leave layout with default view
            return True

        # Get event object
        obj = self.event.object

        # Content portal_type
        obj_type = obj.portal_type
        fti = pt[obj_type]
        available_layouts = fti.getAvailableViewMethods(obj)

        if not (layout in available_layouts):
            self.error(obj, _(u"Layout ${layout} is not available for "
                              u"${portal_type}.",
                       mapping={'layout': layout,
                                'portal_type': obj_type}))
            return False

        # Set Layout
        obj.setLayout(layout)
        return True

    def error(self, obj, message):
        request = getattr(self.context, 'REQUEST', None)
        if request is not None:
            IStatusMessage(request).addStatusMessage(message, type="error")


class SetLayoutAddForm(AddForm):
    """
    An add form for the set layout contentrules action
    """
    form_fields = form.FormFields(ISetLayoutAction)
    label = _(u"Add set layout content rules action")
    description = _(u"An action to set the layout for content items")
    form_name = _(u"Configure action")

    def update(self):
        self.setUpWidgets()
        self.form_reset = False

        data = {}
        errors, action = self.handleSubmit(self.actions, data, self.validate)
        # the following part will make sure that previous error not
        # get overriden by new errors. This is usefull for subforms. (ri)
        if self.errors is None:
            self.errors = errors
        else:
            if errors is not None:
                self.errors += tuple(errors)

        if errors:
            if (len(errors) == 1) and (isinstance(errors[0], ViewFail)):
                # We send a message if validation of view is false and
                # is the only error.
                self.status = _('The view is not available in that container')
                result = action.failure(data, errors)
            else:
                self.status = _('There were errors')
                result = action.failure(data, errors)
        elif errors is not None:
            self.form_reset = True
            result = action.success(data)
        else:
            result = None

        self.form_result = result

    def create(self, data):
        a = SetLayoutAction()
        form.applyChanges(a, self.form_fields, data)
        return a

    def handleSubmit(self, actions, data, default_validate=None):

        for action in actions:
            if action.submitted():
                errors = action.validate(data)
                if errors is None and default_validate is not None:
                    errors = default_validate(action, data)
                return errors, action

        return None, None


class SetLayoutEditForm(EditForm):
    """
    An edit form for the group by date action
    """
    form_fields = form.FormFields(ISetLayoutAction)
    label = _(u"Edit the set layout content rules action")
    description = _(u"An action to set the layout for content items")
    form_name = _(u"Configure action")

    def update(self):
        self.setUpWidgets()
        self.form_reset = False

        data = {}
        errors, action = self.handleSubmit(self.actions, data, self.validate)
        # the following part will make sure that previous error not
        # get overriden by new errors. This is usefull for subforms. (ri)
        if self.errors is None:
            self.errors = errors
        else:
            if errors is not None:
                self.errors += tuple(errors)

        if errors:
            if (len(errors) == 1) and (isinstance(errors[0], ViewFail)):
                # We send a message if validation of view is false and
                # is the only error.
                self.status = _(u'The view is not available in that container')
                result = action.failure(data, errors)
            else:
                self.status = _(u'There were errors')
                result = action.failure(data, errors)
        elif errors is not None:
            self.form_reset = True
            result = action.success(data)
        else:
            result = None

        self.form_result = result

    def handleSubmit(self, actions, data, default_validate=None):

        for action in actions:
            if action.submitted():
                errors = action.validate(data)
                if errors is None and default_validate is not None:
                    errors = default_validate(action, data)
                return errors, action

        return None, None
