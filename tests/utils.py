#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def read_xml(xml_file):
    project_root = os.path.abspath(os.path.dirname(__file__))
    xml_path = os.path.join(project_root, 'xml', xml_file)
    with open(xml_path, "r") as f:
        return f.read()
