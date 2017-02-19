from errbot import BotPlugin, botcmd
from optparse import OptionParser

import logging
import socket
import time
import boto3
log = logging.getLogger(name='errbot.plugins.AWS')

class AWS(BotPlugin):
    
    
    @botcmd(split_args_with=None)
    def ec2_listid(self, msg, args):
        '''list all ec2 instances in account
           option: None
           !ec2 listid
        '''
        idlist = []
        ec2 = boto3.resource('ec2')
        for instance in ec2.instances.all():
            #idlist.append(instance.id)
            return instance.id
