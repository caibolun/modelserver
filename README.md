<!--
 * @Author: ArlenCai
 * @Date: 2022-02-28 23:47:50
 * @LastEditTime: 2022-03-01 12:57:46
-->
# ModelServer: A Simple Socket Server for Model Apply

## Introduce

This is a lightweight process manager for deep learning model deploying by unix socket.

## Usage

### 1. Process config `method/ping.ini`
```
[DEFAULT]
#当收到kill信号后,几秒后干掉worker
graceful_timeout        = 3
#应用的环境变量
base_path               = /home/qspace/data/modelserver
#启动的进程数目,每个进程都是一个实例
number_workers          = 3
#进程名字
proc_name               = ping
#是否需要扔到后端
daemonize               = true
```

### 2. Method handler `method/ping.py`
```
from ModelServer.handler import Handler
class Ping(Handler):
    def __init__(self, cfg, file_logger=None, ppid=None, sockets=None):
        Handler.__init__(self, cfg, file_logger, ppid, sockets)
        self.model = None # model init

    def env_init(self):
        # TODO
        pass

    def apply(self, req):
        # TODO
        resp = req
        return resp
```
> `ModelServer/gpuhelp.py` provides some methods to manage GPU resource, such as `GPULock` and `GetGpuID`.

### 3. Start Server 
```
python server.py -c ./method/ping.ini -e "method.ping:Ping" &
```

### 4. Client Call
```
from ModelServer import Client
client = Client()
ret, resp = client.call('{base_path}/{proc_name}_unix', 'hello world')
print (ret, resp)
```

### 5. Kill Server
```
ps -eo pid,cmd | grep modelserver | grep -v grep | awk -F' ' '{print $1}' | xargs -I{} -t kill -9 {}
```

## Thanks
- gunicorn: https://github.com/benoitc/gunicorn
- ProcessHandler: https://github.com/rfyiamcool/ProcessHandler
