#!/usr/bin/env python

# File: filter-instances.py 
# Description: This is an example script that you can author or modify that retrieves 
#              a list of instances from the Relay Interface (in the form of parameters)
#              and filters the instances that are untagged. It then sets the output
#              variable `instanceIDs` to the list of instances that are untagged. 
# Inputs:
#   - instances - List of instances to evaluate 
# Outputs:
#   - instanceIDs - list of instance IDs to stop in the next step

from relay_sdk import Interface, Dynamic as D

relay = Interface()

to_stop = []

instances = filter(lambda i: i['State']['Name'] == 'running', relay.get(D.instances))
for instance in instances:
    to_stop.append(instance['InstanceId'])
    
print('\nFound {} instances to stop:'.format(len(to_stop)))
print(*[instance_id for instance_id in to_stop], sep = "\n") 

relay.outputs.set('instanceIDs', to_stop)
