#!/usr/bin/env python
# coding=utf-8
'''
Author: ArlenCai
Date: 2022-02-08 21:35:13
LastEditTime: 2022-02-09 10:19:00
'''
import os
import subprocess
import xml.etree.ElementTree as ET
from operator import itemgetter
import fcntl


def GetGpuSmi():
    try:
        smi_res = subprocess.check_output(['nvidia-smi', '-q', '-x'])
    except:
        return None
    smi_res = smi_res.decode('utf-8')
    smi_xml = ET.fromstring(smi_res)
    return smi_xml


def GetGpuID(gpu_mem=2550, gpu_list=[]):
    smi_xml = GetGpuSmi()
    if smi_xml is None:
        return -1

    ok_gpu_list = list()
    for idx, item in enumerate(smi_xml.findall('./gpu/fb_memory_usage')):
        mem_free = item.findtext('free')
        mem_free = int(mem_free.split(' ')[0].strip())
        if mem_free > gpu_mem:
            ok_gpu_list.append({'gpu_id': idx, 'mem_free': mem_free})
    if (ok_gpu_list) == 0:
        return -1

    ok_gpu_list = sorted(
        ok_gpu_list, key=itemgetter('mem_free'), reverse=True)
    gpu_set = set(gpu_list)
    if len(gpu_list) == 0:
        real_gpu_list = [x['gpu_id'] for x in ok_gpu_list]
    else:
        real_gpu_list = [x['gpu_id']
                         for x in ok_gpu_list if x['gpu_id'] in gpu_set]
    if len(real_gpu_list) == 0:
        return -1

    gpu_id = real_gpu_list[0]
    return gpu_id


def GetGpuNames():
    smi_xml = GetGpuSmi()
    if smi_xml is None:
        return []
    product_names = list()
    for _, item in enumerate(smi_xml.findall('./gpu/product_name')):
        product_name = item.text
        product_names.append(product_name)
    return product_names


def ChkGpuName(sub_name):
    product_names = GetGpuNames()
    flag = False
    for _, product_name in enumerate(product_names):
        if sub_name in product_name:
            flag = True
            break
    return flag


class GPULock(object):
    def __init__(self, file_name=""):
        if file_name == "":
            file_name = os.getenv("GPU_LOCK_FILE", "/tmp/GPU_LOCK")
        self.handler = open(file_name, 'wb')

    def __del__(self):
        self.handler.close()

    def lock(self):
        fcntl.flock(self.handler, fcntl.LOCK_EX)

    def unlock(self):
        fcntl.flock(self.handler, fcntl.LOCK_UN)


if __name__ == "__main__":
    lock = GPULock()
    lock.lock()
    print(GetGpuID())
    print(GetGpuNames())
    lock.unlock()
