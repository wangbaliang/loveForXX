#!/usr/bin/env python3
# Time: 2018/12/4 15:46

__author__ = 'wgs@test'


from controller.xxlove.xxlove import FileUploadHandle
from controller.xxlove.xxlove import FileListHandle
from controller.xxlove.xxlove import ClusterListHandle
from controller.xxlove.xxlove import ClusterPaperListHandle
from controller.xxlove.xxlove import SankeyHandle



def register_routes(app):

    app.add_url_rule('/upload', view_func=FileUploadHandle.as_view("upload"), methods=['GET', 'POST'])
    app.add_url_rule('/fileList', view_func=FileListHandle.as_view("fileList"), methods=['GET', 'POST'])
    app.add_url_rule('/clusterList', view_func=ClusterListHandle.as_view("clusterList"), methods=['GET', 'POST'])
    app.add_url_rule('/clusterPaperList', view_func=ClusterPaperListHandle.as_view("clusterPaperList"), methods=['GET', 'POST'])

    app.add_url_rule('/sankey', view_func=SankeyHandle.as_view("sankey"), methods=['GET', 'POST'])
