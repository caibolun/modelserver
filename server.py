#!/usr/bin/env python
# coding=utf-8
'''
Author: ArlenCai
Date: 2022-02-28 22:40:23
LastEditTime: 2022-02-28 23:44:49
'''

import os,sys
from ModelServer import Arbiter
from ModelServer import InitSvrkitLogging
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', action="store", help="Config file path")
    parser.add_argument('-s', '--section', action="store", help="Config file section")
    parser.add_argument('-e', '--extractor', action="store", help="extractor class name")
    parser.add_argument('-i', '--busiconfig', action="store", help="bussiness config file")
    args = parser.parse_args()
    config_file = getattr(args, 'config')
    section = getattr(args, 'section') or "jobexecute"
    extractor = getattr(args, 'extractor')
    busi_config_file = getattr(args, 'busiconfig')
    InitSvrkitLogging(busi_config_file)
    if config_file:
        if config_file[0] != '/':
            config_file = os.path.join(os.getcwd(), os.path.abspath(config_file))
    if not extractor:
        sys.exit(-2)
    Ar = Arbiter(extractor, busi_config_file, config_file, section)
    Ar.run()

if __name__ == '__main__':
    main()
