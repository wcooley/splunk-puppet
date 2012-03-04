#!/usr/bin/env python26
#
# Name: puppethosts.py
# Desc: Splunk search command for parameterizing searches based on Puppet inventory
#

import csv
import httplib
import sys
import yaml

from pprint import pprint as pp

OUTPUT = '/opt/splunk/etc/apps/Puppet/lookups/puppet_hosts.csv'

if __name__ == '__main__':

    conn = httplib.HTTPSConnection('puppet.cic.pdx.edu', port='8140',
            key_file='/tmp/puppet-client.key',
            cert_file='/tmp/puppet-client.crt')


    conn.request('GET', '/production/facts_search/search', None, {'Accept': 'yaml'})

    resp = conn.getresponse()

    if resp.status == 200:
        puppetyaml = resp.read()
        puppet_hosts = yaml.load(puppetyaml)
        puppet_hosts.sort()

        puppet_host_tab = [ (fqdn, fqdn.split('.')[0]) for fqdn in puppet_hosts ]

        csvout = csv.writer(open(OUTPUT, 'w'))

        csvout.writerow(['fqdn', 'host'])
        csvout.writerows(puppet_host_tab)

    else:
        print >>sys.stderr, "Error: Status '%d', Reason '%s'" % ( resp.status, resp.reason)
