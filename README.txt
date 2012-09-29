
**************************************

This is a copy of the Puppet app that is available from
[Splunkbase](http://splunk-base.splunk.com/apps/Splunk+for+Puppet+Configuration+Management)

This is not the original source!

Wil Cooley <wcooley@pdx.edu>
**************************************

Welcome to the Splunk for Puppet App
====================================

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

### Version Monitoring ###

To gather version information, add the following to your manifests (I have it
towards the top of my site.pp, outside of any node definitions):

 `info("node=${hostname} puppetversion=${puppetversion}")`

### CIM Log Reporting ###

Some functionality requires report data from the puppet-cimlog report
processor, written to format and log data for ease of consumption by Splunk.

 https://github.com/wcooley/puppet-cimlog

FIXME Need a lot more here.
