#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : ucsclean.py
@Author: donggangcj
@Date  : 2019/4/1
@Desc  : 
'''
import click

from user.userhelp import main


@click.command()
@click.option('--user', prompt='Enter your user_id', help='Your dce user id')
# @click.option('--database', default='mysql+pymysql://root:O5l@+oDqxl@192.168.1.145:30791/cosmo_portal_ucs',
#               help='The UCS database url')
def clean_dce(user):
    """Simple program that greets NAME for a total of COUNT times."""
    main(user)


if __name__ == '__main__':
    clean_dce()
