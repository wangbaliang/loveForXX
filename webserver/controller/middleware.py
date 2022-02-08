#!/usr/bin/env python3
# Time: 2018/12/6 20:59

__author__ = 'wgs@test'


# import climate
# logging = climate.get_logger(__name__)
import logging
from flask import request, session, jsonify, redirect, url_for


def url_check(app):
    @app.before_request
    def before_request():
        if request.method == 'POST':
            if request.files:
                req_json = request.form
            else:
                req_json = request.get_json(force=True)
                # print('request.path: %s' % request.path)
                # print('request.json: %s' % req_json)
            logging.info('>>>>> [Receive] request.path: %s' % request.path)
            logging.info('>>>>> [Receive] request.json: %s' % req_json)

