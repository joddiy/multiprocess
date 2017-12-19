# -*- coding: utf-8 -*-
# file: example.py
# author: joddiyzhang@gmail.com
# time: 12/12/2017 4:19 PM
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
import random
import time

from multiprocess import MultiProcess, InfoTask, Model


class Demo(Model):
    """
    Task Model
    """

    def runnable(self, *args):
        """
        main function will be executed by Worker
        :param args:
        :return:
        """
        print("run pid", os.getpid(), end=", ")
        print("get first args", args[0], end=", ")
        print("get second args", args[1])
        time.sleep(random.uniform(0, 2))
        return args[0], args[1]

    def callback(self, result):
        """
        callback function when success
        PLEASE NOTE: don't raise any Exception here, otherwise the process cannot exit normally
        :param result:
        :return:
        """
        print("pid", os.getpid(), "result", result[0], result[1])

    def error_callback(self, error):
        """
        callback function when fail
        PLEASE NOTE: don't raise any Exception here, otherwise the process cannot exit normally
        :param error:
        :return:
        """
        print("error_callback ", os.getpid(), error)


if __name__ == '__main__':
    # get a instance of CM module (specify the process-pool size)
    mp = MultiProcess(5)
    # start the CM module
    mp.start()
    for i in range(10):
        # create a Task instance (specify Task module, timeout, args)
        task = InfoTask("example.Demo", 1, {"test": i}, {"error": i})
        # push Task to process-pool
        mp.push(task)
    # no more new Task, wait exit
    mp.stop()
