# codeing=utf-8
import os
import sys
import uuid
import multiprocessing
from threading import Lock
from optparse import OptionParser

# import climate
# climate.enable_default_logging()
# logging = climate.get_logger(__name__)

from flask import Flask, request, render_template

from utils.config_helper import load_all_config, config
load_all_config()

from controller.middleware import url_check
from controller.routes import register_routes
from flask_cors import CORS

from db.db import redis_manager, db_session_manager as db_manager


import logging
formatter_text = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
formatter = logging.Formatter(formatter_text)
logging.basicConfig(level=logging.INFO, format=formatter_text)

app = Flask(__name__)
# app.secret_key = 'Pohoi07t8oFiGo87tUglkj(*&6&%e'

#跨域
CORS(app, supports_credentials=True, origins="*")

register_routes(app)
url_check(app)


@app.route('/doc')
def index():
    return render_template('api-doc-5.0.html')

@app.route('/health')
def test():
    return 'successful'


# if __name__ == '__main__':
db_cfg = config.get('mysql_db.defult')
db_manager.register_db(db_cfg, name='default')
# redis_cfg = config.get('redis_config')
# redis_manager.register_db(redis_cfg, name='default')


if __name__ == '__main__':
    usage = 'usage: python %prog [options] arg1 arg2'
    parser = OptionParser(usage=usage)

    parser.add_option(
        '-g',
        '--debug',
        dest='debug_flag',
        type='int',
        default=99,
        action='store',
        metavar='DEBUG',
        help='debug flag')
    parser.add_option(
        '-i',
        '--ip',
        dest='server_ip',
        type='string',
        # default='0.0.0.0',
        default='127.0.0.1',
        action='store',
        metavar='IP',
        help='pas server ip')
    parser.add_option(
        '-p',
        '--port',
        dest='server_port',
        type='string',
        default='5000',
        action='store',
        metavar='PORT',
        help='pas server port')

    (options, args) = parser.parse_args()


    # set listen '0.0.0.0'
    ip = '0.0.0.0'
    # ip = options.server_ip
    port = int(options.server_port)
    # processes = multiprocessing.cpu_count() if multiprocessing.cpu_count() < 16 else 16
    app.run(host=ip, port=port)
