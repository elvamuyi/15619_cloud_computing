#!/usr/bin/python

import boto
import boto.ec2
import boto.ec2.elb
import boto.ec2.autoscale
import boto.ec2.cloudwatch

import os
import time

# create elb connection
elb_conn = boto.ec2.elb.ELBConnection(
  'AKIAIMMVA5TNRP7KRHKA',
  'hECzayjh4i4baoJTERaZbIzTqZn1eH9GHfkb7Ek3')

elb = elb_conn.get_all_load_balancers()[0]

# create an autoscale connection
as_conn = boto.ec2.autoscale.AutoScaleConnection(
  'AKIAIMMVA5TNRP7KRHKA',
  'hECzayjh4i4baoJTERaZbIzTqZn1eH9GHfkb7Ek3')

lc = as_conn.get_all_launch_configurations(names=['as_launch_configuration'])[0]
ag = as_conn.get_all_groups(['as_group'])[0]


# clean up
ag.shutdown_instances()
while len(as_conn.get_all_autoscaling_instances()) > 0:
  time.sleep(10)

ag.delete()
time.sleep(5)
lc.delete()
elb.delete()
