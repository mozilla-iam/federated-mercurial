"""printparents

Prints the parents of a given revision.
"""

from mercurial import cmdutil, error
from mercurial.i18n import _

cmdtable = {}
command = cmdutil.command(cmdtable)

testedwith = '2.2 2.3'

# Every command must take ui and and repo as arguments.
# opts is a dict where you can find other command line flags.
#
# Other parameters are taken in order from items on the command line that
# don't start with a dash. If no default value is given in the parameter list,
# they are required.
#
# For experimenting with Mercurial in the python interpreter:
# Getting the repository of the current dir:
#    >>> from mercurial import hg, ui
#    >>> repo = hg.repository(ui.ui(), path = ".")

@command('print-parents',
    [('s', 'short', None, _('print short form')),
     ('l', 'long', None, _('print long form'))],
    _('[options] node'))
def printparents(ui, repo, node, **opts):
    # The doc string below will show up in hg help.
    """Print parent information."""
    # repo can be indexed based on tags, an sha1, or a revision number.
    ctx = repo[node]
    parents = ctx.parents()

    try:
        if opts['short']:
            # The string representation of a context returns a smaller portion
            # of the sha1.
            ui.write(_('short %s %s\n') % (parents[0], parents[1]))
        elif opts['long']:
            # The hex representation of a context returns the full sha1.
            ui.write(_('long %s %s\n') % (parents[0].hex(), parents[1].hex()))
        else:
            ui.write(_('default %s %s\n') % (parents[0], parents[1]))
    except IndexError:
        # Raise an Abort exception if the node has only one parent.
        raise error.Abort(_('revision %s has only one parent') % node)