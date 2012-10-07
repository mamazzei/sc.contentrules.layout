# -*- coding: utf-8 -*-

from zope.interface import Interface

from zope.schema import Choice
from sc.contentrules.layout import MessageFactory as _


class ISetLayoutAction(Interface):
    """ Configuration available for this content rule
    """
    layout = Choice(title=_(u"Layout"),
                    description=_(u"Select the layout to be applied"),
                    required=True,
                    vocabulary='sc.contentrules.layout.available_views',)
