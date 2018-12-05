import mercurial.url
import urllib2
import httplib


class FederatedAuthHandler(urllib2.BaseHandler):
    """auth handler for urllib2 that does auth0 OIDC authentication
    """

    handler_order = 480  # what?

    def __init__(self, ui=None, passmgr=None):
        pass

def uisetup(ui):
    if('FederatedAuth' in globals()):
        mercurial.url.handlerfuncs.append(FederatedAuthHandler)
