#!/usr/bin/env python
#
# Name: gendershosts.py
# Desc: Splunk search command for parameterizing searches based on Genders queries
#
# Quickly hacked together by Wil Cooley <wcooley@pdx.edu>
#
# Copyright (C)2013 Will (Wil) Cooley
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
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
