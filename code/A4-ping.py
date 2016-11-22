#!/usr/bin/env python3

from argparse import ArgumentParser

from asynciojobs import Scheduler

# also import the Run class
from apssh import SshNode, SshJob, Run

gateway_hostname  = 'faraday.inria.fr'
gateway_username  = 'onelab.inria.r2lab.tutorial'
gateway_key       = '~/.ssh/onelab.private'

# this time we want to be able to specify the slice on the command line
parser = ArgumentParser()
parser.add_argument("-s", "--slice", default=gateway_username,
                    help="specify an alternate slicename, default={}"
                         .format(gateway_username))
args = parser.parse_args()

# we create a SshNode object that holds the details of
# the first-leg ssh connection to the gateway

# remember to make sure the right ssh key is known to your ssh agent
faraday = SshNode(hostname = gateway_hostname, username = args.slice)

node1 = SshNode(gateway = faraday, hostname = "fit01", username = "root")

check_lease = SshJob(
    # checking the lease is done on the gateway
    node = faraday,
    # this means that a failure in any of the commands
    # will cause the scheduler to bail out immediately
    critical = True,
    command = Run("rhubarbe leases --check"),
)

# the command we want to run in faraday is as simple as it gets
ping = SshJob(
    node = node1,
    # let's be more specific about what to run
    # we will soon see other things we can do on an ssh connection
    command = Run('ping', '-c1',  'google.fr'),
    # this says that we wait for check_lease to finish before we start ping
    required = check_lease,
)

# how to run the same directly with ssh - for troubleshooting
print("""---
for troubleshooting: 
ssh {}@{} ssh root@fit01 ping -c1 google.fr
---""".format(gateway_username, gateway_hostname))

# create an orchestration scheduler with the 2 jobs
# the order here does not matter, only the 'requires' dependencies do
sched = Scheduler(check_lease, ping)

# run the scheduler
ok = sched.orchestrate()

# return something useful to your OS
exit(0 if ok else 1)
