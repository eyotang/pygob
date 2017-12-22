#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import collections

import pytest

import pygob

data = [34, 255, 129, 3, 1, 1, 4, 85, 115, 101, 114, 1, 255, 130, 0, 1, 2, 1, 2, 73, 100, 1, 4, 0, 1, 4, 78, 97, 109, 101, 1, 12, 0, 0, 0, 14, 255, 130, 1, 2, 1, 7, 101, 121, 111, 116, 97, 110, 103, 0]

loader = pygob.Loader()
user = loader.load(bytes(data))
print(user)
data = [14, 255, 130, 1, 6, 1, 7, 101, 121, 111, 116, 97, 110, 103, 0]
user = loader.load(bytes(data))
print(user)

dumper = pygob.Dumper()
result = dumper.dump(user)

print(list(result))
