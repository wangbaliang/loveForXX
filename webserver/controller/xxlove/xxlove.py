#!/usr/bin/env python3
# Time: 2018/12/4 15:49

__author__ = 'wgs@test'


# import climate
# logging = climate.get_logger(__name__)

from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename


from controller.base import Base

import os
import json
import logging
from multiprocessing import Process
import subprocess

from utils.config_helper import config
from utils.sankey import gen_html_path, create_sankey



# 文件上传
class FileUploadHandle(Base):
    def __init__(self):
        super(FileUploadHandle, self).__init__()

    @Base.check_exception
    def post(self):

        f = request.files['file']
        # 项目根目录
        upload_path = os.path.join(config.get("upload_files"), secure_filename(f.filename))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        print("upload_path: ", upload_path)

        # 保存文件包
        f.save(upload_path)

        #插入db记录
        task_id = self.insert_db(upload_path)

        #异步进程解析
        self.aync_process_start(task_id, upload_path)

        return redirect(url_for('upload'))

    def get(self):
        return render_template('upload.html')


    def insert_db(self, upload_path):
        sql = 'insert into source_file_tar(user_name, upload_path) VALUES("%s", "%s")' % (config.get("user_name"), upload_path)
        status, result = self.exec_sql("insert", sql)
        if not status:
            raise Exception("sql error")
        sql = 'select id from source_file_tar order by id desc limit 1'
        status, result = self.exec_sql("select", sql)
        task_id = result[0]['id']
        logging.info("task_id: %s" % task_id)
        return task_id


    def aync_process_start(self, task_id, upload_path):
        p = Process(target=self.p_func, args=(task_id, upload_path))
        p.start()


    def p_func(self, task_id, upload_path):
        logging.info("start task： %s" % task_id)
        _py = config.get("start_py")
        cmd = "python %s %s %s" % (_py, task_id, upload_path)
        code, msg = subprocess.getstatusoutput(cmd)

        print("cmd: ", cmd)
        print("cmd result: ", code, msg)

        # 成功/失败了更新db
        if code == 0:
            sql = "update source_file_tar set status=1 where id=%s" % task_id
        else:
            sql = 'update source_file_tar set status=-1, message="%s" where id=%s' % (msg, task_id)

        status, result = self.exec_sql("update", sql)

        res_dir = os.path.join(config.get("result_json_dir"), id)
        evolution_file = os.path.join(res_dir, "evolution_info.json")
        if os.path.exists(evolution_file):
            create_sankey(task_id, evolution_file)
        else:
            print("task_id: %s 没有解析生成 evolution_info")

        return status, result




# 文件列表
class FileListHandle(Base):
    def __init__(self):
        super(FileListHandle, self).__init__()

    @Base.check_exception
    def get(self):
        id = request.args.get("id")
        if not id:
            sql = "select * from source_file_tar"
        else:
            sql = "select * from source_file_tar where id=%s" % id

        status, infos = self.exec_sql("select", sql)

        return self.set_response(**{'result': infos})



# 文件聚类结果
class ClusterListHandle(Base):
    def __init__(self):
        super(ClusterListHandle, self).__init__()

    @Base.check_exception
    def get(self):
        id = request.args.get("id")
        res_dir = os.path.join(config.get("result_json_dir"), id)
        doc_file = os.path.join(res_dir, "doc_info.json")
        evolution_file = os.path.join(res_dir, "evolution_info.json")

        with open(doc_file) as f:
            doc_res = json.load(f)
        with open(evolution_file) as f:
            evo_res = json.load(f)

        # max_key = max(list(evo_res.keys()))
        # clusters = evo_res.get(max_key)
        years = sorted(evo_res)

        clusters_trans = []
        totol = 0
        for year in evo_res:
            clusters = evo_res[year]

            year_clusters = []
            year_totol = 0

            cluster_classes = sorted(clusters)
            for cluster_class in cluster_classes:
                v = clusters[cluster_class]
                count = len(v['doc_list'])
                year_totol += year_totol
                info = {
                    "cluster_class": cluster_class,
                    "count": count,
                    "keyword_list": v['keyword_list'],
                }
                year_clusters.append(info)

            clusters_trans.append({
                "year": year,
                "count": year_totol,
                "data": year_clusters
            })
            totol += year_totol


        return self.set_response(**{'result': clusters_trans})



# 文件聚类获取文章列表
class ClusterPaperListHandle(Base):
    def __init__(self):
        super(ClusterPaperListHandle, self).__init__()

    @Base.check_exception
    def get(self):
        id = request.args.get("id")
        year = request.args.get("year")
        cluster_class = request.args.get("cluster_class")

        res_dir = os.path.join(config.get("result_json_dir"), id)
        doc_file = os.path.join(res_dir, "doc_info.json")
        evolution_file = os.path.join(res_dir, "evolution_info.json")

        with open(doc_file) as f:
            doc_res = json.load(f)
        with open(evolution_file) as f:
            evo_res = json.load(f)

        clusters = evo_res.get(year)
        item = clusters.get(str(cluster_class))

        result = []

        for id in item.get('doc_list'):
            result.append(doc_res.get(str(id)))

        return self.set_response(**{'result': result})


# 查看桑基图
class SankeyHandle(Base):
    def __init__(self):
        super(SankeyHandle, self).__init__()


    def get(self):

        id = request.args.get("id")
        html_path = gen_html_path(id)
        if not os.path.exists(html_path):
            return self.set_response(**{'status': False, 'message': '桑基图路径不存在: %s' % html_path})
        html_path = os.path.split(html_path)[1]
        return render_template(html_path)