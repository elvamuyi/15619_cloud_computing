#!/usr/bin/python

import boto
import boto.ec2
import boto.ec2.elb
import boto.ec2.autoscale
import boto.ec2.cloudwatch

import os
import time

AVAILABLE_ZONE = 'us-east-1d' ##
AMI_ID = 'ami-2b7b2c42'       ##
INSTANCE_TYPE = 'm1.medium'
MIN_SIZE = 1
MAX_SIZE = 8
DESIRED_SIZE = 3

# create elb connection
elb_conn = boto.ec2.elb.ELBConnection(
  'AKIAIMMVA5TNRP7KRHKA',
  'hECzayjh4i4baoJTERaZbIzTqZn1eH9GHfkb7Ek3')

# create new elb and configure health check
zones = [AVAILABLE_ZONE]
ports = [(80,80,'http')]
elb = elb_conn.create_load_balancer('elb-for-as-group', zones, ports)
hc = boto.ec2.elb.HealthCheck(interval=20,
                              timeout=5,
                              unhealthy_threshold=2,
                              healthy_threshold=10,
                              target='HTTP:80/')
elb.configure_health_check(hc)
elb_dns = elb.dns_name

# create an autoscale connection
as_conn = boto.ec2.autoscale.AutoScaleConnection(
  'AKIAIMMVA5TNRP7KRHKA',
  'hECzayjh4i4baoJTERaZbIzTqZn1eH9GHfkb7Ek3')

# create a launch configuration
lc = boto.ec2.autoscale.launchconfig.LaunchConfiguration(
  name='as_launch_configuration',
  image_id=AMI_ID,
  instance_type=INSTANCE_TYPE,
  security_groups=['SSH_HTTP'],
  instance_monitoring=True)
as_conn.create_launch_configuration(lc)
lc = as_conn.get_all_launch_configurations(names=['as_launch_configuration'])[0]

# create a Tag for the austoscale group
tag1 = boto.ec2.autoscale.tag.Tag(key='15619_Group', value = 'Alvin', propagate_at_launch=True, resource_id='as_group')
tag2 = boto.ec2.autoscale.tag.Tag(key='15619_Step', value = '6', propagate_at_launch=True, resource_id='as_group')

# create an auto scaling group
ag = boto.ec2.autoscale.group.AutoScalingGroup(
  name='as_group',
  launch_config=lc,
  availability_zones=[AVAILABLE_ZONE],
  load_balancers=['elb-for-as-group'],
  desired_capacity=DESIRED_SIZE,
  tags=[tag1,tag2],
  max_size=MAX_SIZE,
  min_size=MIN_SIZE)
as_conn.create_auto_scaling_group(ag)
ag = as_conn.get_all_groups(['as_group'])[0]

# configure auto scaling group to send notifications
ag.put_notification_configuration(
  'arn:aws:sns:us-east-1:337494561394:Project2_Auto_Scaling',
  ['autoscaling:EC2_INSTANCE_LAUNCH', 'autoscaling:EC2_INSTANCE_TERMINATE'])

# create auto scale policies
scale_out_policy = boto.ec2.autoscale.policy.ScalingPolicy(
  name='ScaleOut',
  as_name='as_group',
  scaling_adjustment=1,
  adjustment_type='ChangeInCapacity')
scale_in_policy = boto.ec2.autoscale.policy.ScalingPolicy(
  name='ScaleIn',
  as_name='as_group',
  scaling_adjustment=-1,
  adjustment_type='ChangeInCapacity')

as_conn.create_scaling_policy(scale_out_policy)
as_conn.create_scaling_policy(scale_in_policy)

scale_out_policy = as_conn.get_all_policies(policy_names=['ScaleOut'])[0]
scale_in_policy = as_conn.get_all_policies(policy_names=['ScaleIn'])[0]

# create cloudwatch alarms
cw = boto.ec2.cloudwatch.CloudWatchConnection(
  aws_access_key_id='AKIAIMMVA5TNRP7KRHKA',
  aws_secret_access_key='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')

alarm_dimensions = {"AutoScalingGroupName": 'as_group'}

scale_up_alarm = boto.ec2.cloudwatch.alarm.MetricAlarm(
  name='scale_up_on_cpu',
  metric='CPUUtilization',
  namespace='AWS/EC2',
  statistic='Average',
  comparison='>',
  threshold=70,
  period=60,
  evaluation_periods=1,
  dimensions=alarm_dimensions,
  alarm_actions=[scale_out_policy.policy_arn])

scale_down_alarm = boto.ec2.cloudwatch.alarm.MetricAlarm(
  name='scale_down_on_cpu',
  metric='CPUUtilization',
  namespace='AWS/EC2',
  statistic='Average',
  comparison='<',
  threshold=30,
  period=60,
  evaluation_periods=1,
  dimensions=alarm_dimensions,
  alarm_actions=[scale_in_policy.policy_arn])

cw.create_alarm(scale_up_alarm)
cw.create_alarm(scale_down_alarm)

# wait until there's some instance in service on elb
#while str(elb.get_instance_health()).find('InService') == -1:
#  time.sleep(5)
#time.sleep(30)

# in service ... ...
# in service ... ...

# clean up
#ag.shutdown_instances()
#while len(as_conn.get_all_autoscaling_instances()) > 0:
#  time.sleep(10)

#ag.delete()
#time.sleep(5)
#lc.delete()
#elb.delete()
