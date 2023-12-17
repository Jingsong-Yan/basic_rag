# coding=utf-8
# Filename:    main_service_online.py
# Author:      ZENGGUANRONG
# Date:        2023-09-10
# description: tornado服务启动核心脚本

import tornado.ioloop
from tornado.web import RequestHandler, Application
from tornado.httpserver import HTTPServer
from tornado.options import options, define
from multiprocessing import Process

from src.searcher.searcher import Searcher
from src.models.vec_model import VectorizeModel
from src.server.handlers.search_handler import SearcherHandler,StartSearcherHandler
from src.server.handlers.vec_model_handler import VecModelHandler,StartVecModelHandler

def launch_service(config):
    searcher = Searcher(config["process_searcher"]["VEC_MODEL_PATH"], config["process_searcher"]["VEC_INDEX_DATA"])
    process_searcher = Process(target=StartSearcherHandler, args=(config["process_searcher"], searcher))
    # vec_model = VectorizeModel(config["process_vec_model"]["VEC_MODEL_PATH"])
    # process_vec_model = Process(target=StartVecModelHandler, args=(config["process_vec_model"], vec_model))

    # processes = [process_searcher, process_vec_model]
    processes = [process_searcher]
    for process in processes:
        process.start()
    for process in processes:
        process.join()


if __name__ == "__main__":
    config = {"process_searcher":{"port":9090, 
                                      "url_suffix":"/searcher", 
                                      "VEC_MODEL_URL":"http://127.0.0.1:9091/a",
                                      "VEC_MODEL_PATH":"C:/work/tool/huggingface/models/simcse-chinese-roberta-wwm-ext",
                                      "VEC_INDEX_DATA":"vec_index_test2023121301_20w"},
             "process_vec_model":{"port":9091, 
                                      "url_suffix":"/vec_model", 
                                      "VEC_MODEL_PATH":"C:/work/tool/huggingface/models/simcse-chinese-roberta-wwm-ext"}}
    launch_service(config)