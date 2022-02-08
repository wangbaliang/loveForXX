# -*- coding: utf-8 -*-
# wgs@test

# Build-in

import hashlib
import json
import os
import sys
import time
import uuid
import zipfile
import arrow
import zlib
# import climate
import requests
import shutil
import subprocess
import traceback
import logging


# climate.enable_default_logging()
# logging = climate.get_logger(__name__)


def exec_cmd(cmd, mode='system'):
    cmd = cmd + " 2>&1"
    if mode == 'system':
        # logging.info('Cmd: %s', cmd)
        return os.system(cmd)
    elif mode == 'subprocess':
        # logging.info('Cmd: %s', ' '.join(cmd))
        return subprocess.call(cmd)

def get_uuid():
    return uuid.uuid1().hex


def check_path_dos_file(path):

    def _dos2unix(file_path):
        # logging.info('Dos to unix file: %s', file_path)
        bin_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'bin/dos2unix')
        cmd = '%s %s' % (bin_path, file_path)
        exec_cmd(cmd)
        return

    for dir_path, dir_names, file_names in os.walk(path):
        for f_name in file_names:
            if f_name.split('.')[-1] not in ['py', 'sh']:
                continue
            file_path = os.path.join(dir_path, f_name)
            _dos2unix(file_path)


def _md5(src_str=''):
    md5_info = hashlib.md5()
    if src_str:
        md5_info.update(src_str.encode("utf8"))
    return md5_info.hexdigest()


def md5_passwd(password, salt=None):
    if (not password) or not isinstance(password, str):
        return None, None
    if not salt:
        salt = _md5()
    last_passwd = _md5(password+salt)

    return last_passwd, salt


def store_2_json(data, file_path):
    with open(file_path, 'w') as json_file:
        json_file.write(json.dumps(data))


def load_json(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data


def http_request(url, params=None, data=None, request_type='post',
                 login_auth=None, timeout=None, files=None, verify=None, token=None):

    # logging.info('[Request] url: %s' % url)
    # logging.info('[Request] json: %s' % data)
    session = requests.Session()
    headers = {
        'Content-Type': 'application/json', 'Accept': 'application/json'}
    if token:
        headers['token'] = token

    try_num = 0
    while True:
        try:
            if files:
                response = session.request(
                    request_type, url, params=params, data=data,
                    files=files, verify=verify)
            else:
                response = session.request(
                    request_type, url, params=params, json=data, headers=headers, verify=verify)
            logging.info('[Receive] response: %s json: %s' % (response, response.json()))
            return response
        except requests.exceptions.ConnectionError as e:
            # logging.error('[HttpRequest] connect server error: %s, retry' % traceback.format_exc())
            try_num += 1
            if try_num < 3:
                time.sleep(1)
            else:
                raise Exception(str(e))


def normalizeDirName(path, type='dir'):
    if not path or len(path) < 1:
        return None
    if not isinstance(path, str):
        return None
    if path[0] == '~':
        path = os.environ['HOME'] + path[1:]
    while path[-1:] == os.path.sep:
        path = path[:-1]
    if type == 'file':
        if not os.path.isfile(path):
            return None
    else:
        if not os.path.isdir(path):
            return None
    return os.path.abspath(path)


#打包目录为zip文件（未压缩）
def make_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)
            #相对路径      zipf.write(pathfile, arcname)  zipf.close()
            zipf.write(pathfile, arcname)
    zipf.close()


def unzip(filename, out_dir):
     r = zipfile.is_zipfile(filename)
     if r:
         starttime = time.time()
         fz = zipfile.ZipFile(filename,'r')
         for file in fz.infolist():
             print(file.filename)  # 打印zip归档中目录
             d = file.date_time
             gettime = "%s/%s/%s %s:%s" % (d[0], d[1], d[2], d[3], d[4])
             fz.extract(file, out_dir)
             filep = os.path.join(out_dir, file.filename)
             # print("恢复文件:%s的最后修改时间" % filep)
             timearry = time.mktime(time.strptime(gettime, '%Y/%m/%d %H:%M'))
             os.utime(filep, (timearry, timearry))
         endtime = time.time()
         times = endtime - starttime
         print('unzip %s times: ' % filename + str(times))
     else:
         print('This file is not zip file')
     return True


class ProjectPathManager(object):

    def __init__(self):
        self.base_project_path = os.path.join(os.path.dirname(
            os.path.dirname((os.path.abspath(__file__)))), 'user_projects/')

    def generate_work_path(self, user_name, type='ml'):
        tag = arrow.now('+08:00').format('YYYY_MM_DD_HH_mm_ss_') + user_name + '_' + type
        project_dir = os.path.join(self.base_project_path, tag)
        if not os.path.exists(project_dir):
            os.mkdir(project_dir)
        return project_dir

    def generate_work_path_notime(self, user_id, type='ml'):
        tag = user_id + '_' + type
        project_dir = os.path.join(self.base_project_path, tag)
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
        return project_dir

    def check_real_project_dir(self, train_base_dir):
        files = os.listdir(train_base_dir)
        if len(files) == 1:
            path = os.path.join(train_base_dir, files[0])
            if os.path.isdir(path):
                return path
        else:
            return train_base_dir

    def remove_path(self, path):
        filelist = os.listdir(path)
        for f in filelist:
            filepath = os.path.join(path, f)
            if os.path.isfile(filepath):
                os.remove(filepath)
            elif os.path.isdir(filepath):
                shutil.rmtree(filepath, True)


def dict_processing(dict, args):
    for key, value in args.items():
        dict[key] = value
    return dict



def crc32(filepath):
    block_size = 1024 * 1024
    crc = 0
    fd = open(filepath, 'rb')
    while True:
        buffer = fd.read(block_size)
        if len(buffer) == 0: # EOF or file empty. return hashes
            fd.close()
            if sys.version_info[0] < 3 and crc < 0:
                crc += 2 ** 32
            # 返回的是十六进制的字符串
            return hex(crc)
        crc = zlib.crc32(buffer, crc)

