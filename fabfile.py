import os
import yaml
from fabric.contrib.files import exists
from fabric.api import cd, env, run, sudo, task, shell_env

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def loadenv(filepath = os.path.join(__location__, 'vars.yml')):
    """Cargar las variables del fichero vars.yml"""
    with open(filepath, 'r') as f:
        return yaml.load(f)

env.config = loadenv()
env.password = env.config['vm_password']
PROJECT_NAME = env.config['project_name']
PROJECT_ROOT = '%s/%s' % (env.config['install_root'], PROJECT_NAME)
PROJECT_REPO = env.config['project_repo']
host = env.config['vm_user'] + '@' + env.config['vm_name'] + '.cloudapp.net'
env.hosts = [host]
env.environment = 'production'


def get_repo():
    if exists(PROJECT_ROOT + '/' + '.git'):
        run('cd %s && git pull origin master' % (PROJECT_ROOT))
    else:
        run('git clone %s %s' % (PROJECT_REPO, PROJECT_ROOT))


def restart_gunicorn():
    "Reiniciar gunicorn"
    sudo('/etc/init.d/gunicorn restart')

def restart_nginx():
    "Reiniciar nginx"
    sudo('service nginx restart')


@task
def deploy(): 
    """Desplegar la aplicacion"""
    sudo('mkdir -p {}'.format(PROJECT_ROOT))
    sudo('chown -R {}:{} {}'.format(env.config['vm_user'], env.config['vm_user'], PROJECT_ROOT))

    with cd(PROJECT_ROOT):
        get_repo()
        with shell_env(EN_PROD='{}'.format(env.config['EN_PROD']), SECRET_KEY='{}'.format(env.config['SECRET_KEY']), DATABASE_URL='{}'.format(env.config['DATABASE_URL'])):
            sudo('make install_prod')
            run('make migrate_')
            run('make populate')
            run('make staticfiles')

    restart_gunicorn()
    restart_nginx()
