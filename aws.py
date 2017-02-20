from errbot import BotPlugin, botcmd
from optparse import OptionParser

import logging
import socket
import time
import boto3
log = logging.getLogger(name='errbot.plugins.AWS')

class AWS(BotPlugin):
    def _ec2_find_instance(self, name):
        for instance in ec2.instances.all():
            for i in instance.tags:
                if i['Key'] == 'Name':
                    insname = i['Value']
            if name == insname or name == instance.id:
                return instance
    def _ec2_instance_details(self, name):
        instance = self._ec2_find_instance(name)
        if instance is not None:
            if ec2.SecurityGroup(instance.security_groups[0]['GroupId']).tags is not None:
                    for i in security_group.tags:
                        if i['Key'] == 'Name':
                            sec_gp = i['Value']
            details = {
                'id' : instance.id,
                'status' : instance.state['Name'],
                'ip_private' : instance.private_ip_address,
                'ip_public'  : instance.public_ip_address,
                'security_group' : sec_gp,            
                'instance_type': instance.instance_type
            }
        else:
            details = {'error': 'instance named {0} not found.'.format(name)}
        return details
    @botcmd(split_args_with=None)
    def ec2_list(self, msg, args):
        '''list all ec2 instances in account
           option: None
           !ec2 list
        '''
        ec2 = boto3.resource('ec2')
        for instance in ec2.instances.all():
            #idlist.append(instance.id)
            #yield instance.id
            for i in instance.tags:
                if i['Key'] == 'Name':
                    name = i['Value']
            self.send(msg.frm,
                      '{0}: {1}'.format(instance.id, name),
                      message_type=msg.type,
                      in_reply_to=msg,
                      groupchat_nick_reply=True) 
    @botcmd(split_args_with=None)
    def ec2_info(self, msg, args):
        '''provide info of ec2 instances
           option: instance id or name
           Example: !ec2 info i-0aa26058860a003d4
                    !ec2 info docker-machine
        '''
        name = args.pop(0)
        details = self._ec2_instance_details(name)
        self.send(msg.frm,
                  '{0} : {1}'.format(name, details),
                  message_type=msg.type,
                  in_reply_to=msg,
                  group_nick_reply=True)    
    
    
    
    
    
    
    
    
    
    
    
    
    
    