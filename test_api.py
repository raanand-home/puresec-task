import requests
import pytest
import subprocess
import time
import os
import uuid
import signal

HOST='http://localhost:5001'
@pytest.fixture(autouse=True)
def api():
    if 'DOCKER_RUN' not in os.environ:
        raise 'sdf'
        with subprocess.Popen('python3 web-service/app.py', shell=True, preexec_fn=os.setsid) as pro:
            time.sleep(3)
            yield
            pro.kill()
            os.killpg(os.getpgid(pro.pid), signal.SIGHUP)
            os.killpg(os.getpgid(pro.pid), signal.SIGKILL)
            os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
    else:
        global HOST
        HOST = 'http://localhost:5001'
        yield


def random_string():
    return str(uuid.uuid4())


class RequestFactory():
    def __init__(self):
        self.arn = random_string()
        self.name = random_string()
        self.runtime = 'python'
        self.memory = 128
        self.total_time = 123
        self.used_memory = 213
        self.security_insepect_time = 2
        self.cpu_presentage = 21.0
        self.finnish_state = 'Success'
        self.application = random_string()

    def send(self):
        response = requests.post(
            HOST + '/execute',
            json={
                'arn': self.arn,
                'func_info': {
                    'name': self.name,
                    'runtime': self.runtime,
                    'memory': self.memory
                },
                'runtime_info': {
                    "total_time": self.total_time,
                    "security_insepect_time": self.security_insepect_time,
                    "cpu_presentage": self.cpu_presentage,
                    "used_memory": self.used_memory,
                    "finnish_state": self.finnish_state,
                    "application": self.application,
                }
            }
        )
        response.raise_for_status()


class QueryFactory():
    def __init__(self):
        pass


def test_execute():
    factory = RequestFactory()
    factory.send()
    factory.send()


def test_excecute_and_query():
    factory = RequestFactory()
    factory.total_time = 200
    factory.send()
    factory.total_time = 100
    factory.send()
    response = requests.post( HOST + '/query',
        json={
            'filters': {
                'arn': factory.arn },
            'what':
                'total_time'

        }
    )
    response.raise_for_status()
    assert response.json()['result'] == 150
