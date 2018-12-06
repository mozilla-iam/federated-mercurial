"""oidcauth

authenticate to an oidc provider
"""

from mercurial import cmdutil, error
from mercurial.i18n import _

cmdtable = {}
command = cmdutil.command(cmdtable)

testedwith = '2.2 2.3'

@command('oidcauth',[])
def oidcauth(ui, repo, node, **opts):
    #ctx = repo[node]
    ui.write(_('hello world\n'))