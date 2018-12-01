import os
import pytest
import subprocess
import testinfra

@pytest.fixture(scope='session')
def host(request):
    subprocess.check_call(['docker', 'build', '-t', 'image-under-test', '.'])
    docker_id = subprocess.check_output(['docker', 'run', '--rm', '-d', '--entrypoint=/usr/bin/tail', '-t', 'image-under-test']).decode().strip()
    
    yield testinfra.get_host("docker://" + docker_id)
    
    # teardown
    subprocess.check_call(['docker', 'rm', '-f', docker_id])

def test_system(host):
    assert host.system_info.distribution == 'alpine'
    assert host.system_info.release == '3.8.1'

def test_entrypoint(host):
    entrypoint = '/usr/local/bin/entrypoint.sh'
    assert host.file(entrypoint).exists
    assert oct(host.file(entrypoint).mode) == '0o555'

def test_user(host):
    user = 'flickr'
    assert host.user(user).uid == 3999
    assert host.user(user).gid == 3999
    assert host.user(user).shell == '/bin/false'

def test_app_folder(host):
    folder = '/app'
    assert host.file(folder).exists
    assert host.file(folder).user == 'flickr'
    assert host.file(folder).group == 'flickr'
    assert oct(host.file(folder).mode) == '0o500'

def test_config_folder(host):
    folder = '/config'
    assert host.file(folder).exists
    assert host.file(folder).user == 'flickr'
    assert host.file(folder).group == 'flickr'
    assert oct(host.file(folder).mode) == '0o500'

@pytest.mark.parametrize('package', [
    ('python3'),
    ('su-exec'),
])
def test_installed_dependencies(host, package):
    assert host.package(package).is_installed
