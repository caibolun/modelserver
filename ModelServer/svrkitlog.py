#!/usr/bin/env python
# coding=utf-8
'''
Author: ArlenCai
Date: 2022-02-28 23:13:43
LastEditTime: 2022-03-01 12:45:34
'''
import configparser
import logging


def InitSvrkitLogging(conf_path):
    
    fmt = '[%(levelname)1.1s %(asctime)s %(process)d %(name)s %(funcName)s:%(lineno)d] %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'

    try:
        busi_cfg = configparser.ConfigParser()
        busi_cfg.read([conf_path,])
        conf_log = busi_cfg['Log']
        conf_server = busi_cfg['Server']
        module_name = conf_server['ModuleName']
        from svrkit_core.log import Handler, GetLoggingLevel, COMM_LOG_DEBUG
        qs_log_level = COMM_LOG_DEBUG #conf_log['QSLogLevel']
        log_level = GetLoggingLevel(qs_log_level)
        osslog_hdl = Handler(module_name, qs_log_level, conf_log['QSLogFilePath'], \
            attach_module_shm=conf_log['LogShmSeparateByModuleMode'], open_net_log=conf_log['LogShmIsOpenNetLog'])
        logging.basicConfig(format=fmt, datefmt=datefmt, level=log_level, handlers=[osslog_hdl])
    except:
        logging.basicConfig(format=fmt, datefmt=datefmt, level=logging.NOTSET, filename="/tmp/modelserver.log", filemode="w") 
    return
