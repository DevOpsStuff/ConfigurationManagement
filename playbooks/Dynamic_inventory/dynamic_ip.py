#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import socket
import subprocess
import pprint

def main():
    for dyn in inventory():
        print(json.dumps(dyn,sort_keys=True, indent=2))

def inventory():
    ips = find_pi()
    json_list = []
    for ip in ips:
    
       xyz =  {
          'all': {
              'hosts': [ip],
              'vars': {},
          },
          '_meta': {
              'hostvars': {
                  ip: {
                     'ansible_ssh_user': 'ansible',
                  }
              },
          },
          'ansible': [ip]
       }
 
       json_list.append(xyz)

    return json_list


def find_pi():
    ip_address = []
    for ip in all_local_ips():
        if port_22_is_open(ip):
           ip_address.append(str(ip))
    return ip_address


def all_local_ips():
    lines = subprocess.check_output(['arp', '-a']).split('\n')
    for line in lines:
        if '(' not in line:
            continue
        after_open_bracket = line.split('(')[1]
        ip = after_open_bracket.split(')')[0]
        yield ip


def port_22_is_open(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    result = sock.connect_ex((ip, 22))
    return result == 0


if __name__ == '__main__':
    main()

