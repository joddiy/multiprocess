# -*- coding: utf-8 -*-
# file: info_task.py
# author: joddiyzhang@gmail.com
# time: 11/12/2017 5:35 PM
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


class InfoTask(object):
    """
    common Task
    """
    from_pid, task_module, timeout, args = None, None, None, None

    def __init__(self, task_module, timeout, *args):
        """
        init function
        :param task_module: task module path(eg: src.components.multiprocess.example.Demo)
                            if it is False, it means there isn't any more new Task
        :param timeout: timeout (second)
        :param args: other params transferred to module
        """
        self.from_pid = os.getpid()
        self.task_module = task_module
        self.timeout = timeout
        self.args = args
