# -*- coding: utf-8 -*-
# file: demo.py
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


def runnable(*args):
    print("run", os.getpid(), args[0])
    time.sleep(random.uniform(0, 2))
    return args[0], args[0]


def callback(*result):
    print("result ", os.getpid(), result[0])


def error_callback(error):
    print("error_callback ", os.getpid(), error)
