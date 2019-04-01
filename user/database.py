#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : database.py
@Author: donggangcj
@Date  : 2019/4/1
@Desc  : 
'''

from contextlib import contextmanager
from logging import getLogger

from sqlalchemy import create_engine, MetaData, Column, BigInteger, String
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

LOG = getLogger(__name__)

DATABASE_URL = 'mysql+pymysql://root:O5l@+oDqxl@192.168.1.145:30791/cosmo_portal_ucs'

engine = create_engine(DATABASE_URL,
                       pool_recycle=3600,
                       max_overflow=20,
                       echo=False,
                       encoding="utf8",
                       connect_args={'charset': 'utf8'})

md = MetaData(bind=engine)
Base = automap_base()


class Team(Base):
    __tablename__ = 't_ucs_user_team'

    user_id = Column(BigInteger, primary_key=True)
    team_name = Column(String(255), primary_key=True)
    # __table_args__ = (
    #     PrimaryKeyConstraint('user_id', 'team_name'),
    # )


class Tenant(Base):
    __tablename__ = 't_ucs_team_tenant'

    cluster_id = Column(BigInteger, primary_key=True)
    tenant_name = Column(String(255), primary_key=True)


Base.prepare(engine, reflect=True)
User = Base.classes.t_ucs_user
Cluster = Base.classes.t_ucs_cluster


@contextmanager
def sqlalchemy_session():
    session = sessionmaker(bind=engine, expire_on_commit=False)()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.expunge_all()
        session.close()
