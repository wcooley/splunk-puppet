Puppet Pulse App for Splunk
===========================

This app should give insight into the health and functioning of your Puppet
installation.

The Views
---------

The views are the following:

 * Overview
 * Changes
 * Statistics
 * Agent Anomalies

The different views should be self-explanatory.

Installation & Setup
--------------------
### Prerequisites ###

 * A working Puppet master & agents, with logs being indexed by Splunk, either
   with a Splunk forwarder reading local logs or a central syslog collector.

 * A working Splunk installation.

### App Setup ###

The following are explanations of setup options within Splunk's app setup.

#### Puppet Hosts ####

The script `bin/puppethosts.py` connects to the Puppet master's inventory
service to generate a list of known hosts which have been managed by Puppet.
For this script to work, it needs to be able to read the private key of the
host on which it is running, which it should be able to do if Splunk is running
as root. If Splunk is not running as root, other arrangements have to be
made--giving the Splunk user read access to the key, creating a separate key &
cert in ~splunk/.puppet, etc.

Also, the Puppet master must be configured to permit the Splunk server access
to the `/facts` endpoint, with an entry in `/etc/puppet/auth.conf` such as:

    path /facts
    auth yes
    method find, search
    allow splunkhost.example.com

More information about configuring Puppet's inventory service can be found at
http://docs.puppetlabs.com/guides/inventory_service.html#configuring-access

If you cannot or do not want to use this, you can replace the default, `|
puppethosts`, with something like `| inputlookup puppethosts.csv` and upload a
CSV with columns 'host,fqdn' (where 'host' is the short host name).

#### Puppet Events ####

This should be the narrowest search which will include all of your Puppet
events -- ideally it will include at least either a `source` or `sourcetype`.
If your Puppet events are in a non-default index, include this here. All other
eventtypes, macros and saved searches (should) use this.

#### Agent, Master & CIM Log Events ####

These final searches should differentiate agent, master and cimlog events. I
have an extraction for the process name, so am able to match on
`process=puppet-agent` and such, but I am uncertain if this was a default
extraction or one I configured. If you do not have this, then just matching on
'puppet-agent' or 'puppet-master' should suffice. Note that the agent & master
searches should exclude cimlog events.

Other Setup
-----------

#### CIM Log Reporting ####

Some functionality requires report data from the puppet-cimlog report
processor, written to format and log data for ease of consumption by Splunk.

 https://github.com/wcooley/puppet-cimlog

#### Version Reporting ####

To gather version information, add the following to your manifests (I have it
towards the top of my site.pp, outside of any node definitions):

    info("node=${hostname} puppetversion=${puppetversion}")

#### Commit Tracking ####

If your Puppet master config is managed with Git, `misc/git-hook-post-update`
is a post-update hook which logs commits as they enter your repository, which
can be useful for narrowing down which commit started causing errors.

To use, copy it to the `$MASTER_REPO.git/hooks/` or `/etc/puppet/.git/hooks`
directory of your Puppet master repository and ensure it is executable. (I use
the former directory, but I expect that the latter works too, but consider how
the commit log time stamps will relate to Puppet events.)

Sample scripts for other VCSs would be a welcome contribution.

#### Splunk Free vs Enterprise ####

The free version of Splunk does not include summary indexing, which is used (or
will be) to present graphs of long-term data trends. Some manual configuration
will likely be necessary, possibly commenting out saved searches using
summary-index data and uncommenting searches using directly searched data (also
with a much narrower time range).

History
-------

This app started as a copy of the Splunk for Puppet app by Simon Yanick and
grew from there. At this point, much has been replaced and eventually all
should be.
