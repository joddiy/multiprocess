# -*- coding: utf-8 -*-
# file: multiprocess.py
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
    common multiprocess module
    """
    pool_num, parent_conn, child_conn, pro = None, None, None, None

    def __init__(self, pool_num=10):
        """
        Init function
        :param pool_num: process-pool size
        """
        self.pool_num = pool_num

    def start(self):
        """
        Start a sub-process which manages the process-pool of Worker, and connects with its parent-process by pipeline.
        Parent-processor will send Task to sub-process which then gets a process from pool to execute it.
        :return:
        """
        # print("===> now start parent, PID:", os.getpid())
        # parent-process start a server process, and sub-process will be started by this server, avoid thread-unsafe
        # set_start_method('forkserver')
        self.parent_conn, self.child_conn = Pipe()
        self.pro = Process(target=self._start_pool, args=(self.child_conn,))
        self.pro.start()

    def push(self, task):
        """
        Push Task to pipeline
        :return:
        """
        self.parent_conn.send(task)

    def stop(self):
        """
        Wait exit
        :return:
        """
        # push exit signal to pipeline
        self.push(InfoTask(False, 1))
        # wait sub-process exit
        self.pro.join()
        # close pipeline
        self.parent_conn.close()
        self.child_conn.close()

    def _start_pool(self, child_conn):
        """
        Start a process-pool, and then connect parent-process by pipeline.
        After get a task, it will assign a worker to execute it.
        :param child_conn:
        :return:
        """
        # print("===> now start child, PID:", os.getpid())
        pool = multiprocessing.Pool(processes=self.pool_num)
        while True:
            # hold and wait task
            info_task = child_conn.recv()
            if info_task.task_module is False:
                # when receive False, exit
                break
            else:
                task_module = importlib.import_module(info_task.task_module)
                # start a worker
                monitor_func = partial(self.monitor_worker, task_module.runnable, timeout=info_task.timeout)
                pool.apply_async(monitor_func, args=info_task.args, callback=task_module.callback,
                                 error_callback=task_module.error_callback)
        pool.close()
        pool.join()

    @staticmethod
    def monitor_worker(func, *args, **kwargs):
        """
        Worker process will start a thread to excute Task, and another to monitor whether it is timeout.
        :param func:
        :param args:
        :param kwargs:
        :return:
        """
        # print("===> now task get a worker, PID:", os.getpid())
        timeout = kwargs.get('timeout', None)
        # start a thread to monitor
        p = ThreadPool(1)
        res = p.apply_async(func, args=args)
        try:
            # wait result
            out = res.get(timeout)
            return out
        except multiprocessing.TimeoutError:
            # exit when timeout
            p.terminate()
            raise Exception("timeout", args)
        except Exception as e:
            # other error
            p.terminate()
            raise Exception(str(e), args)
