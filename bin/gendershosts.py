#!/usr/bin/env python
#
# Name: gendershosts.py
# Desc: Splunk search command for parameterizing searches based on Genders queries
#
# Quickly hacked together by Wil Cooley <wcooley@pdx.edu>
#

import re
import sys
from subprocess import PIPE, STDOUT
import subprocess

def err(msg="Undetermined error"):
    print "ERROR"
    print msg
    sys.exit(0)

if __name__ == '__main__':

    if len(sys.argv) < 2:
        genders_query = '~NONE' # Trick to list all hosts
    else:
        genders_query = sys.argv[1]

    if len(sys.argv) > 2:
        header = sys.argv[2]
    else:
        header = "host"

    if re.search('[^\w\d&|~\-()=:\.]', genders_query):
        err("Inappropriate character in Genders query")

    hosts = subprocess.Popen( ['/usr/bin/nodeattr', '-n', genders_query], \
            stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).communicate()[0]

    print header
    print hosts,
