# -*- coding: utf-8 -*-
# file: 
# author: joddiyzhang@gmail.com
# time: 11/12/2017 5:07 PM
# Copyright (C) <2017>  <Joddiy Zhang>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------
import os
import importlib
import multiprocessing
from functools import partial
from multiprocessing import Pool, Pipe, Process, set_start_method
from multiprocessing.pool import ThreadPool
from .info_task import InfoTask


class MultiProcess(object):
    """
    通用多进程类
    """
    pool_num, parent_conn, child_conn, pro = None, None, None, None

    def __init__(self, pool_num=10):
        """
        初始化
        :param pool_num:进程池子容量
        """
        self.pool_num = pool_num

    def start(self):
        """
        开启一个子进程，该此子进程管理 Worker 进程池，父进程与子进程通过管道通信
        父进程将任务发送给子进程，子进程分配给进程池进行执行
        :return:
        """
        print("===> now start parent, PID:", os.getpid())
        # 开启一个服务器进程，统一由服务器进程产生子进程，避免线程不安全
        # set_start_method('forkserver')
        self.parent_conn, self.child_conn = Pipe()
        self.pro = Process(target=self._start_pool, args=(self.child_conn,))
        self.pro.start()

    def push(self, task):
        """
        向管道推送任务
        :return:
        """
        self.parent_conn.send(task)

    def stop(self):
        """
        等待退出
        :return:
        """
        # 向管道推送结束信号
        self.push(InfoTask(False, 1))
        # 等待子进程退出
        self.pro.join()
        # 关闭管道
        self.parent_conn.close()
        self.child_conn.close()

    def _start_pool(self, child_conn):
        """
        开启进程池，并通过管道和父进程通信，接受到任务之后分配给进程池执行
        :param child_conn:
        :return:
        """
        print("===> now start child, PID:", os.getpid())
        pool = multiprocessing.Pool(processes=self.pool_num)
        while True:
            # 阻塞并接受任务
            info_task = child_conn.recv()
            if info_task.task_module is False:
                # 接受到的任务方法为 False 的时候退出
                break
            else:
                task_module = importlib.import_module(info_task.task_module)
                # 开启 worker 执行任务
                monitor_func = partial(self.monitor_worker, task_module.runnable, timeout=info_task.timeout)
                pool.apply_async(monitor_func, args=info_task.args, callback=task_module.callback,
                                 error_callback=task_module.error_callback)
        pool.close()
        pool.join()

    @staticmethod
    def monitor_worker(func, *args, **kwargs):
        """
        worker 进程中开启一个线程执行任务，本线程监控是否超时
        :param func:
        :param args:
        :param kwargs:
        :return:
        """
        print("===> now task get a worker, PID:", os.getpid())
        timeout = kwargs.get('timeout', None)
        # 开启一个线程进行监控
        p = ThreadPool(1)
        res = p.apply_async(func, args=args)
        try:
            # 等待执行结果
            out = res.get(timeout)
            return out
        except multiprocessing.TimeoutError:
            # 超时退出
            p.terminate()
            raise Exception("timeout", args)
        except Exception as e:
            # 其他异常
            p.terminate()
            raise Exception(str(e), args)
