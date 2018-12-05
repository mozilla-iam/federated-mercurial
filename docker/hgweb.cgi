#!/usr/bin/env python

config = "/etc/hgweb.conf"
#import sys; sys.path.insert(0, "/path/to/python/lib")
#import cgitb; cgitb.enable()
from mercurial import demandimport; demandimport.enable()
from mercurial.hgweb import hgweb, wsgicgi

application = hgweb(config)
wsgicgi.launch(application)
