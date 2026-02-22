import random
import threading
import socket
import psutil
import pickle
import queue
import tarfile
import shutil
import json
import yaml
import os
from argparse import ArgumentParser, Namespace



class ThreadPool():
    # 线程池
    def __init__(self, maxsize = 8):
        self.pool = queue.Queue(maxsize)   # 使用queue队列，创建一个线程池
        for _ in range(maxsize):
            self.pool.put(threading.Thread)

    def get_thread(self):
        return self.pool.get()

    def add_thread(self):
        self.pool.put(threading.Thread)


class MultiThreadingRun():
    # 多线程运行自定义函数
    # try_mode开启的情况下，setthread内的自定义function会使用try来运行，使得function即使失败也不中断主进程，线程也能正常回收
    def __init__(self, threadpoolmaxsize=8, try_mode=False):
        self.threadpool = ThreadPool(threadpoolmaxsize)
        self.global_thread_lock = threading.Lock()
        self.try_mode = try_mode

    def runwiththreadlock(self, function, **kwargs):
        # 用法举例：
        # def testdef(a, b, c):
        #     print('Sum:', a + b + c)
        # multithread = mytoolbox.MultiThreadingRun(2)
        # multithread.runwiththreadlock(testdef, a=1, b=2, c=3)
        with self.global_thread_lock:
            function(**kwargs)

    def setthread(self, function, **kwargs):
        # 用法举例：
        # def testdef(a, b, c):
        #     print('Sum:', a + b + c)
        # multithread = mytoolbox.MultiThreadingRun(2)
        # multithread.setthread(testdef, a=1, b=2, c=3)
        def tempfunction():
            if self.try_mode:
                try:
                    function(**kwargs)
                except:
                    pass
            else:
                function(**kwargs)
            self.threadpool.add_thread()
        readythread = self.threadpool.get_thread()
        process = readythread(target=tempfunction)
        process.start()

    def ifthreadpoolfull(self):
        return self.threadpool.pool.full()


def killprocesswithpid(pid):
    # 通过进程pid杀掉进程，如果有子进程也会递归杀掉子进程后再杀掉进程
    # pid为int类型
    target_process = psutil.Process(pid)
    for child_process in target_process.children():
        killprocesswithpid(child_process.pid)
    target_process.kill()

def checkifslurmjobinqueue(slurm_job_uid, temp_file_save_dir):
    # 通过slurm job uid检查目前这个job是否处于slurm队列中(无论是R/PD/CG等任意状态)
    os.system('squeue -j ' + (str)(slurm_job_uid) + ' | grep ' + (str)(slurm_job_uid) + ' > ' + os.path.join(os.path.normpath(temp_file_save_dir), 'temp_slurm_queue_check_result_' + (str)(slurm_job_uid) + '.txt'))
    with open(os.path.join(os.path.normpath(temp_file_save_dir), 'temp_slurm_queue_check_result_' + (str)(slurm_job_uid) + '.txt'), 'r') as f:
        content = f.readlines()
    os.remove(os.path.join(os.path.normpath(temp_file_save_dir), 'temp_slurm_queue_check_result_' + (str)(slurm_job_uid) + '.txt'))
    if (len(content) > 0):
        return True
    else:
        return False

def scanusableport(port_list):
    # 从port_list中查找一个能用的port并返回
    random.shuffle(port_list)
    def checkport(port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('localhost', port))
            s.close()
            return True
        except:
            return False
    for port in port_list:
        if checkport(port):
            return port
    return None

def list_union(list_a, list_b):
    # 求两个python列表的并集
    return list(set(list_a).union(set(list_b)))

def list_intersection(list_a, list_b):
    # 求两个python列表的交集
    return list(set(list_a).intersection(set(list_b)))

def list_difference(list_a, list_b):
    # 求两个python列表的差集，返回list_a - list_b
    return list(set(list_a).difference(set(list_b)))

def args2dict(source_args):
    # 将args转换为dict格式
    return vars(source_args)

def dict2args(source_dict):
    # 将dict转换为args格式
    return Namespace(**source_dict)

def savetojson(savingdata, filename, ifprint=True):
    # 将中间数据存储为json，适合列表、字典、字符串等
    # 文件若已存在会自动覆盖
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, 'w') as f:
        json.dump(savingdata, f, indent=4)
    if ifprint:
        print('Saving', filename, 'done!', flush=True)

def readjson(filename):
    # 读取存储在json中的数据
    with open(filename, 'r') as f:
        savingdata = json.load(f)
    return savingdata

def savebypickle(savingdata, filename, ifprint=True):
    # 将中间数据使用pickle存储为二进制文件
    # 文件若已存在会自动覆盖
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, 'wb') as f:
        pickle.dump(savingdata, f)
    if ifprint:
        print('Saving', filename, 'done!', flush=True)

def readpicklefile(filename):
    # 读取使用pickle存储的文件
    with open(filename, 'rb') as f:
        savingdata = pickle.load(f)
    return savingdata

def savetoyaml(savingdata, filename, ifprint=True):
    # 将中间数据存储为yaml
    # 文件若已存在会自动覆盖
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, 'w') as f:
        yaml.dump(data=savingdata, stream=f, allow_unicode=True, sort_keys=False)
    if ifprint:
        print('Saving', filename, 'done!', flush=True)

def readyaml(filename):
    # 读取yaml文件
    with open(filename, 'r') as f:
        savingdata = yaml.load(f.read(), Loader=yaml.FullLoader)
    return savingdata

def unpacktargz(filename, remove_source_file=False, ifprint=True):
    # 解压缩tar.gz文件到当前目录
    if ((len(filename) <= 7) or (filename[-7:] != '.tar.gz')):
        if ifprint:
            print(filename, 'is not a tar.gz file...', flush=True)
        return False

    filepath = os.path.dirname(filename)

    try:
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        with tarfile.open(filename, 'r:gz') as f:
            f.extractall(path=filepath)
    except:
        if ifprint:
            print(filename, 'unpack failed...', flush=True)
        if os.path.exists(filename[:-7]):
            shutil.rmtree(filename[:-7])
        return False

    if remove_source_file:
        os.remove(filename)
    if ifprint:
        print(filename, 'unpack success...', flush=True)
    return True

def packtotargz(foldername, remove_source_folder=False, ifprint=True):
    # 压缩指定文件夹为tar.gz
    sourcefoldername = os.path.normpath(foldername)
    packname = os.path.basename(sourcefoldername)

    try:
        with tarfile.open(sourcefoldername + '.tar.gz', 'w:gz') as f:
            f.add(sourcefoldername, arcname=packname)
    except:
        if ifprint:
            print(sourcefoldername, 'pack to tar.gz failed...', flush=True)
        if os.path.exists(sourcefoldername + '.tar.gz'):
            os.remove(sourcefoldername + '.tar.gz')
        return False

    if remove_source_folder:
        shutil.rmtree(sourcefoldername)
    if ifprint:
        print(sourcefoldername + '.tar.gz', 'pack success...', flush=True)
    return True