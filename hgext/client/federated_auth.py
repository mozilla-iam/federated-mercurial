"""oidcauth

authenticate to an oidc provider
"""

from mercurial import cmdutil, error
from mercurial.i18n import _

cmdtable = {}
command = cmdutil.command(cmdtable)

testedwith = '2.2 2.3'
def retrieve_well_known(well_known_url):
    resp = requests.get(well_known_url)
    data = resp.json()
    return data['token_endpoint'], data['authorization_endpoint']


@command('oidcauth',[])
def oidcauth(ui, repo, node, **opts):
    #ctx = repo[node]
    ui.write(_('here we go!\n'))

    # load up config

    # init login flow

    # get the response

    # post the response to kang


