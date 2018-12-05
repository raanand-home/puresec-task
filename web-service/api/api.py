from sqlalchemy.exc import IntegrityError
import logging
from app import Session
from dal import register_function
from dal import is_function_registered
from dal import FunctionStatus
from dal import add_execution
from dal import query_avarage


def execute(execute_information):
    arn = execute_information['arn']
    
    func_info = execute_information['func_info']
    try:
        if not is_function_registered(arn):
            register_function(
                arn=arn,
                name=func_info['name'],
                runtime=func_info['runtime'],
                memory=func_info['memory'])
    except IntegrityError:
        logging.info('This is allowed race condition')
    runtime_info = execute_information['runtime_info']
    str_function_status = runtime_info['finnish_state']
    if str_function_status == 'Success':
        finnish_state = FunctionStatus.Success
    elif str_function_status == 'Failed':
        finnish_state = FunctionStatus.Failed
    elif str_function_status == 'Timeout':
        finnish_state = FunctionStatus.Timeout
    add_execution(arn=arn,
                  total_time=runtime_info['total_time'],
                  security_insepect_time=runtime_info['security_insepect_time'],
                  cpu_presentage=runtime_info['cpu_presentage'],
                  used_memory=runtime_info['used_memory'],
                  finnish_state=finnish_state,
                  application=runtime_info['application'])


def query(query_information):
    what = query_information['what']
    return dict(result=query_avarage(what,**query_information['filters']))
