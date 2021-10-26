#!/usr/bin/env python

from relay_sdk import Interface, Dynamic as D

relay = Interface()

to_stop = []

instances = filter(lambda i: i['State']['Name'] == 'running', relay.get(D.instances))
for instance in instances:
    try:
        to_stop.append(instance['InstanceId'])
    except Exception as e:
            print('\nEC2 instance {0} not considered for termination because of a processing error: {1}'.format(instance['InstanceId'], e)) 

print('\nFound {} instances to stop:'.format(len(to_stop)))
print(*[instance_id for instance_id in to_stop], sep = "\n") 

relay.outputs.set('instanceIDs', to_stop)
