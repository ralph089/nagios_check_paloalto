#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_check_paloalto
----------------------------------

Tests for `check_paloalto` modules.
"""

import os

import pytest


@pytest.fixture(scope="session")
def read_xml(xml_file):
    project_root = os.path.abspath(os.path.dirname(__file__))
    xml_path = os.path.join(project_root, 'xml', xml_file)
    with open(xml_path, "r") as f:
        return f.read()
