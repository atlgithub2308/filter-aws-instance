#!/usr/bin/env python

from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from relay_sdk import Interface, Dynamic as D
import logging

logging.basicConfig(level=logging.WARNING)

relay = Interface()

credentials = ClientSecretCredential(
    client_id=relay.get(D.azure.connection.clientID),
    client_secret=relay.get(D.azure.connection.secret),
    tenant_id=relay.get(D.azure.connection.tenantID)
)
subscription_id=relay.get(D.azure.connection.subscriptionID)
compute_client = ComputeManagementClient(credentials, subscription_id)

# Getting resource ids & options
resource_ids = []

# If resource group is specified, find VMs under that resource group.
rg = ''
try:
  rg=relay.get(D.resourceGroup)
except:
  print('No resource group found. Looking up all Virtual Machines under subscription id.')

if (rg):
 print('Looking up all Virtual Machines under resource group {0}:'.format(rg))
 virtual_machines = compute_client.virtual_machines.list(rg)

# Get all VMs under a Subscription ID
else: 
  virtual_machines = compute_client.virtual_machines.list_all()

# Append VM resource IDs to list
print ("\n{:<30} {:<30} {:<30} {:<30}".format('NAME', 'LOCATION', 'VM SIZE', 'TAGS')) 
for virtual_machine in virtual_machines:
  print("{:<30} {:<30} {:<30} {:<30}".format(virtual_machine.name, virtual_machine.location, virtual_machine.hardware_profile.vm_size, str(virtual_machine.tags)))
  resource_ids.append(virtual_machine.id)

# Setting output variable `virtualMachines` to list of Azure Virtual Machines
print('Setting output `virtualMachines` to list of {0} found virtual machines'.format(len(resource_ids)))


print('Starting {} Azure Virtual machine(s)'.format(len(resource_ids)))

# Deletes each VM in resource_id list 
vm_handle_list = []
for resource_id in resource_ids:
  resource_group_name = resource_id.split('/')[4] # Resource group name
  vm_name = resource_id.split('/')[8] # VM name
  print('Starting Azure Virtual Machine {0} in Resource Group {1}'.format(vm_name, resource_group_name))  
  async_vm_operation = compute_client.virtual_machines.begin_start(resource_group_name, vm_name)
  vm_handle_list.append(async_vm_operation)

wait = True

# If wait is set, wait for VMs to terminate before exiting.
if wait: 
  for async_vm_operation in vm_handle_list:
    print('Waiting for Azure Virtual Machine to be started.')
    async_vm_operation.wait()

print('All specified Azure Virtual Machines are started.')
