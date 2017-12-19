# -*- coding: utf-8 -*-
# file: mp_model.py
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
    main function will be executed by Worker
    :param args:
    :return:
    """
    pass


def callback(result):
    """
    callback function when success
    PLEASE NOTE: don't raise any Exception here, otherwise the process cannot exit normally
    :param result:
    :return:
    """
    pass


def error_callback(error):
    """
    callback function when fail
    PLEASE NOTE: don't raise any Exception here, otherwise the process cannot exit normally
    :param error:
    :return:
    """
    pass
