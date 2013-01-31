#!/usr/bin/env python26
#
# Name: puppethosts.py
# Desc: Splunk search command for generating lookup table of puppet hosts
#
# This command could also be used to search the Puppet inventory
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

import csv
import httplib
import json
import socket
import subprocess
import sys

from pprint import pprint as pp
from subprocess import PIPE, STDOUT

from splunk import Intersplunk as si

def puppet_config(key):
    return exec_read_line(['puppet', 'agent', '--configprint', key])

def exec_read_line(args):
    return subprocess.Popen(args,
                            stdin=PIPE,
                            stdout=PIPE,
                            stderr=STDOUT,
                            close_fds=True).communicate()[0].rstrip()


if __name__ == '__main__':

    puppet_private_key  = puppet_config('hostprivkey')
    puppet_client_cert  = puppet_config('hostcert')
    puppet_master       = puppet_config('inventory_server')
    puppet_master_port  = puppet_config('inventory_port')

    conn = httplib.HTTPSConnection(puppet_master,
                            puppet_master_port,
                            key_file=puppet_private_key,
                            cert_file=puppet_client_cert)


    conn.request('GET', '/production/facts_search/search', None, {'Accept': 'pson'})

    resp = conn.getresponse()

    if resp.status == 200:
        puppet_hosts = json.loads(resp.read())
        puppet_hosts.sort()

        puppet_host_tab = [ dict((('fqdn',fqdn), ('host',fqdn.split('.')[0]))) \
                            for fqdn in puppet_hosts ]

        si.outputResults(puppet_host_tab)

    else:
        si.generateErrorResults("Error: Status '%d', Reason '%s'" % (resp.status, resp.reason))
