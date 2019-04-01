#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : userhelp.py
@Author: donggangcj
@Date  : 2019/3/25
@Desc  : 删除DCE中用户、租户、团队、及其之间的授权关系
         数据库中删除对应的表关系
'''
import logging

from user.database import User, sqlalchemy_session, Team, Tenant, Cluster
from user.dce import DceClient


def _delete_user(user_id):
    """
    delete the user from t_ucs_user
    :param user_id:
    """
    with sqlalchemy_session() as session:
        user = session.query(User).filter(User.user_id == user_id).one_or_none();
        if user:
            logging.info(user)
            session.delete(user)
            session.commit()
            logging.info("USER:{} delete successfully".format(user_id))


def _delete_team(user_id):
    """
    delete the user_team from t_ucs_user_team
    :param user_id: user id from haier user center
    """
    with sqlalchemy_session() as session:
        team = session.query(Team).filter(Team.user_id == user_id).one_or_none()
        if team:
            session.delete(team)
            session.commit()
            logging.info("USER_TEAM:{} delete successfully".format(user_id))


def _delte_tenant(cluster_id, tenant_name, team_name):
    """
    delte the team_tenant from t_ucs_team_tenant
    :param cluster_id: dce host ip
    :param tenant_name: u+`team_name`
    :param team_name: user id from haier user center
    """
    with sqlalchemy_session() as session:
        tenant = session.query(Tenant).filter_by(cluster_id=cluster_id, team_name=team_name,
                                                 tenant_name=tenant_name).one_or_none()
        if tenant:
            session.delete(tenant)
            session.commit()
            logging.info(
                "TEAM_TENANT:cluster_id-{},team-{},tenant-{} delete successfully".format(cluster_id, team_name,
                                                                                         tenant_name))


def get_cluster():
    """
    get the dce clusters configuration from database
    :return:
    """
    with sqlalchemy_session() as session:
        clusters = session.query(Cluster).all()
        return clusters


def main(user_indentity):
    logging.basicConfig(level=logging.INFO)
    logging.info("======DCE USER HELPER======")
    logging.info("USER INDENTITY:{}".format(user_indentity))

    logging.info('======CLEANING DCE INFORMATION======')
    for cluster in get_cluster():
        logging.info('')
        logging.info("=====CLUSTER_ID:{}".format(cluster.cluster_id))
        dceclient = DceClient(cluster.cluster_ip, cluster.cluster_key, cluster.cluster_secret,
                              cluster_id=cluster.cluster_id)

        dceclient.remove_user(user_indentity)
        dceclient.remove_team(user_indentity)
        dceclient.remove_tenant(user_indentity)
        dceclient.remove_registry(user_indentity)

    logging.info('')
    logging.info('======CLEANING DATABASE======')
    _delete_user(user_indentity)
    _delete_team(user_indentity)
    for cluster in get_cluster():
        _delte_tenant(cluster.cluster_id, 'u' + user_indentity, user_indentity)

    logging.info('')
    logging.info("======UCS CLEANING SUCCESSFULLY======")
