#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : apphelpers.py
@Author: donggangcj
@Date  : 2019/3/25
@Desc  : 删除指定租户下的app
'''

import logging

import requests

auth = ('admin', 'changeme')
base_uri = 'http://192.168.1.100'

app_list = requests.get(base_uri + '/dce/apps', headers={'X-DCE-TENANT': 'u2005021426'}, auth=auth)

print(app_list.json())

for item in app_list.json().get('items'):
    print(item.get('metadata').get('name'))
    requests.delete(base_uri + '/dce/apps/{}'.format(item.get('metadata').get('name')),
                    headers={'X-DCE-TENANT': 'u2005021426'}, auth=auth)

if __name__ == '__main__':
    logging.info("======DCE APP HELP========")
