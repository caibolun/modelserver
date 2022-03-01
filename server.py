#!/usr/bin/env python
# coding=utf-8
'''
Author: ArlenCai
Date: 2022-02-28 22:40:23
LastEditTime: 2022-03-01 12:30:33
'''

from ModelServer import Arbiter, InitSvrkitLogging
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', action="store", help="Config file path")
    parser.add_argument('-e', '--extractor', action="store", help="extractor class name")
    parser.add_argument('-i', '--busiconfig', action="store", help="bussiness config file")
    args = parser.parse_args()
    config_file = getattr(args, 'config')
    extractor = getattr(args, 'extractor')
    busi_config_file = getattr(args, 'busiconfig')
    InitSvrkitLogging(busi_config_file)
    
    Ar = Arbiter(extractor, config_file)
    Ar.run()

if __name__ == '__main__':
    main()
