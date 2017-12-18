# -*- coding: utf-8 -*-
# file: 
# author: joddiyzhang@gmail.com
# time: 11/12/2017 6:03 PM
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


def runnable(*args):
    """
    交给worker 执行的方法
    :param args:
    :return:
    """
    pass


def callback(*result):
    """
    执行成功后的调用
    :param result:
    :return:
    """
    pass


def error_callback(error):
    """
    执行失败后的调用
    :param error:
    :return:
    """
    pass
