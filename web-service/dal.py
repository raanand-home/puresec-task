import logging
import enum
from app import Session
from entities import Function, Execution
from sqlalchemy import func
from sqlalchemy.sql import exists

def is_function_registered(arn):
    session = Session()
    return session.query(exists().where(Function.arn == arn)).scalar()


def register_function(arn, name, runtime, memory):
    session = Session()
    session.add(Function(arn=arn, name=name, runtime=runtime, memory=memory))
    session.commit()


class FunctionStatus(enum.IntEnum):
    Success = 0
    Failed = 1
    Timeout = 2


def add_execution(arn,
                  total_time,
                  security_insepect_time,
                  cpu_presentage,
                  used_memory,
                  finnish_state,
                  application):
    session = Session()

    session.add(Execution(function=arn,
                          total_time=total_time,
                          security_insepect_time=security_insepect_time,
                          cpu_presentage=cpu_presentage,
                          used_memory=used_memory,
                          finnish_state=finnish_state,
                          application=application))
    session.commit()


def query_avarage(what,
                  arn=None,
                  finnish_state=None,
                  application=None):
    session = Session()
    query = session.query(
        func.avg(getattr(Execution,what)).label('average')
    )
    if arn is not None:
        query = query.filter(Execution.function == arn)
    if finnish_state is not None:
        query = query.filter(Execution.finnish_state == finnish_state)
    if application is not None:
        query = query.filter(Execution.application == application)

    return query.first()[0]
