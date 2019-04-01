#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : dce.py
@Author: donggangcj
@Date  : 2019/4/1
@Desc  : 
'''
import logging

import requests


class DceClient(requests.Session):
    """The DCE API Client

    Package the DCE open api to transfer Conveniently

    Attributes:
        base_url: A string url of the dce controller
        key: A string of dce administrator's access_key
        secret: A string of dce administrator's access_secret
        cluster_id: A string of dce

    """

    def __init__(self, base_url, key, secret, cluster_id=None):
        super(DceClient, self).__init__()
        self.base_url = base_url
        self.auth = (key, secret)
        self.cluster_id = cluster_id

    def request(self, method, url, **kwargs):
        modified_url = self.base_url + url
        return super(DceClient, self).request(method, modified_url, **kwargs)

    def remove_tenant(self, user_id):
        """
        remove the dce tenant if tenant existed

        :param user_id:
        :return:
        """
        path = '/dce/tenants/{}'.format('u' + user_id)
        result = self.get(path)
        if result.status_code == 200:
            if self.delete(path, params={'force': True}).status_code == 200:
                logging.debug("Tenant:{} delete successfully".format('u' + user_id))
                return True
            else:
                return False

    def remove_team(self, user_id):
        """
        remove the dce team if team existed

        :param user_id:
        :return:
        """

        team_result = self.get('/dce/teams', params={'All': True})
        team_id = list(item.get("Id") for item in team_result.json() if item.get('Name') == user_id)[0]

        path = '/dce/teams/{}'.format(team_id)
        result = self.get(path)
        if result.status_code == 200:
            logging.debug(result.json())
            if self.delete(path, params={'force': True}).status_code == 200:
                logging.debug("Team:{} delete successfully".format('u' + user_id))
                return True
            else:
                return False

    def remove_user(self, user_id):
        """
        remove the dce user if user existed

        :param user_id:
        :return:
        """
        path = '/dce/accounts/{}'.format(user_id)
        result = self.get(path)
        if result.status_code == 200:
            if self.delete(path).status_code == 200:
                logging.debug("User:{} delete successfully".format('u' + user_id))
                return True
            else:
                return False

    def remove_registry(self, registry_name):
        """
        remove the dce user if user existed

        :param registry_name:
        :return:
        """
        path = '/dce/registries/buildin-registry/namespaces/{}'.format(registry_name)
        result = self.get(path)
        if result.status_code == 200:
            if self.delete(path).status_code == 200:
                logging.debug("Registry:{} delete successfully".format(registry_name))
                return True
            else:
                return False
