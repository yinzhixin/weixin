#coding:utf-8

from fabric.api import *
from fabric.context_managers import *
from fabric.colors import *
from fabric.contrib.console import confirm
import time
import os


#服务器账户密码相同时，采用如下形式，如果密码为空，则在部署过程中会提示输入服务器密码
env.user = 'root'
env.password = ''
env.hosts = [
    '123.56.26.7'
]
'''
#服务器账户密码不同时，可采用如下形式
env.passwords = {
    'root@123.56.26.7:22': 'xxxxxx'
}
#定义服务器分组
env.roledefs = {
    'webservers': ['123.56.26.7'],
    'dbservers': ['123.56.26.7']
}
'''

#本地源码路径，env添加自定义变量
#env.project_dev_source = "F:\\mycode\\fabric\\source\\"
env.project_dev_source = "F:\\mycode\\django-pai\\"
#本地打包路径
env.project_tar_source = "F:\\mycode\\release\\"
#打包名称
env.project_tar_name = "release.tar.gz"

#服务器项目根目录，env添加自定义变量
env.deploy_project_root = "/yinzhixin"
#服务器发布目录，位于主目录下边
env.deploy_release_dir = "/myblog"
#服务器对外目录，实际为发布目录的软连接，位于主目录下边
env.deploy_project_current = "/current"
#项目版本号
env.deploy_version = time.strftime("%Y%m%d",time.localtime()) + "_v1"


@runs_once
def tar_except_static():
    """装饰器修饰，打包函数只需执行一次，打包除了静态文件"""
    print yellow("Creating source package....")
    with lcd(env.project_dev_source):
        #我本地装了tar for windows，支持tar命令，但是不支持压缩不能打包为gzip格式，故打包命令不加 -z参数
        local("tar cvf %s . -X extstatic.txt" % (env.project_tar_source+env.project_tar_name))
        #linux参考如下命令
        #local("tar czvf %s ." % env.project_tar_source+env.project_tar_name)
    print green("Create package successfully!")


@runs_once
def tar_static():
    """只打包静态文件"""
    print yellow("Creating source package....")
    with lcd(env.project_dev_source):
        #我本地装了tar for windows，支持tar命令，但是不支持压缩不能打包为gzip格式，故打包命令不加 -z参数
        local("tar cvf %s root_static" % (env.project_tar_source+env.project_tar_name))
        #linux参考如下命令
        #local("tar czvf %s ." % env.project_tar_source+env.project_tar_name)
    print green("Create package successfully!")

@runs_once
def tar_source():
    """全量打包"""
    print yellow("Creating source package....")
    with lcd(env.project_dev_source):
        #我本地装了tar for windows，支持tar命令，但是不支持压缩不能打包为gzip格式，故打包命令不加 -z参数
        local("tar cvf %s . -X ext.txt" % (env.project_tar_source+env.project_tar_name))
        #linux参考如下命令
        #local("tar czvf %s ." % env.project_tar_source+env.project_tar_name)
    print green("Create package successfully!")

@task   #task修饰符使该函数在命令行针对fab可执行
def put_source():
    """将项目包上传服务器并解压缩"""
    print yellow("Ready to upload the source package...")

    with settings(warn_only= True):
        with cd('/'):
            run("mkdir -p %s" % (env.deploy_project_root+env.deploy_release_dir))   #建立多级目录
    env.deploy_full_path = env.deploy_project_root + env.deploy_release_dir
    print yellow("Uploading the source package...")
    with settings(warn_only=True):
        result = put(env.project_tar_source+env.project_tar_name, env.deploy_full_path)
    if result.failed and not confirm("put file failed,Continue[Y/N]?"):
        abort("Aborting to upload!")
    with cd(env.deploy_full_path):
        run("tar -xvf %s" % env.project_tar_name)
        time.sleep(5)
        run("rm -rf %s" % env.project_tar_name)
    print green("Upload&untar successfully!")


@task
def make_symlink():
    """建立项目软连接"""
    print yellow("Update current symlink!")
    env.deploy_full_path = env.deploy_project_root + env.deploy_release_dir + '/' + \
        env.deploy_version
    with settings(warn_only= True):
        run("rm -rf %s" % (env.deploy_project_root+env.deploy_project_current))
        run("ln -s %s %s" % (env.deploy_full_path, env.deploy_project_root+env.deploy_project_current))
    print green("Finish make symlink and deploy successfully!")


@task
def roll_back():
    """发布失败时，版本回滚"""
    print yellow("Rollback project version...")
    versionid = raw_input("please enter the rollback versionid:")
    env.deploy_full_path = env.deploy_project_root+env.deploy_release_dir+'/' + \
        versionid
    with settings(warn_only=True):
        run("rm -rf %s" % (env.deploy_project_root + env.deploy_project_current))
        run("ln -s %s %s" % (env.deploy_full_path, env.deploy_project_root+env.deploy_project_current))
    print green("Rollback successfully!")


@task
def restart_service():
    """停起应用，使发布生效"""
    print yellow("Stoping the uwsgi and nginx service...")
    with settings(warn_only=True):
        run("fuser -k 80/tcp")
        run("fuser -k 9090/tcp")
    print yellow("Restarting the service.....")
    with settings(warn_only=True):
        run("uwsgi --ini /etc/uwsgi9090.ini -d /yinzhixin/myblog/logs/uwsgi.log")
        run("/usr/local/nginx-1.5.6/sbin/nginx")
    print green("Deploy successfully!")


@task
def deploy():
    """发布调用入口，windows本机亲测可行"""
    #tar_source()
    #tar_static()
    tar_except_static()
    put_source()
    restart_service()
    #make_symlink()







