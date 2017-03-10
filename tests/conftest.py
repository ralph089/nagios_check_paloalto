#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pytest

import check_pa.modules.throughput


@pytest.yield_fixture(scope="function")
def statefile(delete = True):
    statefile_path = check_pa.modules.throughput.get_statefile_path()
    yield statefile_path
    try:
        os.remove(statefile_path)
    except OSError:
        pass


