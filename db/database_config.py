import configparser
import os
config = configparser.ConfigParser()
rootDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(rootDir, 'config.ini')

try:
    config.read(configPath)
except Exception as e:
    print('读取数据库配置错误')
    exit(-1)


def get_host():
    return config.get('mysql', 'host')


def get_password():
    return config.get('mysql', 'password')


def get_db_name():
    return config.get('mysql', 'dbName')
