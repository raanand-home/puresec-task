from dal import *
import uuid


def generate_unique_arn():
    return str(uuid.uuid4())


def test_add_function():
    register_function(generate_unique_arn(), 'sdf', '213', 123)

def query_avarage_security_insepect_time(*args,**kwargs):
	return query_avarage('security_insepect_time', *args,  **kwargs)

def test_add_executeand_query():
    arn = generate_unique_arn()
    register_function(arn, 'sdf', '213', 123)
    add_execution(arn=arn,
                  total_time=200,
                  security_insepect_time=10,
                  cpu_presentage=0.1,
                  used_memory=12,
                  application="app",
                  finnish_state=FunctionStatus.Success)
    add_execution(arn=arn,
                  total_time=200,
                  security_insepect_time=20,
                  cpu_presentage=0.1,
                  used_memory=12,
                  application="app",
                  finnish_state=FunctionStatus.Failed)
    q = query_avarage_security_insepect_time(arn=arn)
    assert q == 15.0


def test_add_executeand_query_with_finnish_status_filter():
    arn = generate_unique_arn()
    register_function(arn, 'sdf', '213', 123)
    add_execution(arn=arn,
                  total_time=200,
                  security_insepect_time=10,
                  cpu_presentage=0.1,
                  used_memory=12,
                  application="app",
                  finnish_state=FunctionStatus.Success)
    add_execution(arn=arn,
                  total_time=200,
                  security_insepect_time=20,
                  cpu_presentage=0.1,
                  used_memory=12,
                  application="app",
                  finnish_state=FunctionStatus.Failed)
    q = query_avarage_security_insepect_time(
        arn=arn,
        finnish_state=FunctionStatus.Success)
    assert q == 10.0

def test_add_executeand_query_with_finnish_with_application_filter():
    arn = generate_unique_arn()
    register_function(arn, 'sdf', '213', 123)
    add_execution(arn=arn,
                  total_time=200,
                  security_insepect_time=10,
                  cpu_presentage=0.1,
                  used_memory=12,
                  application="app",
                  finnish_state=FunctionStatus.Success)
    add_execution(arn=arn,
                  total_time=200,
                  security_insepect_time=20,
                  cpu_presentage=0.1,
                  used_memory=12,
                  application="app2",
                  finnish_state=FunctionStatus.Failed)
    q = query_avarage_security_insepect_time(
        arn=arn)
    assert q == 15.0
    q = query_avarage_security_insepect_time(
        arn=arn,
        application='app')
    assert q == 10.0