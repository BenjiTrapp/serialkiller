#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = 'Bruno Adelé <bruno@adele.im>'
__copyright__ = 'Copyright (C) 2013 Bruno Adelé'
__description__ = """timeseries database with reduce system"""
__license__ = 'GPL'
__version__ = '0.0.1'

import struct

from serialkiller.sktypes import default


class ulong(default):
    """Generic Class for type"""
    def __init__(self, **kwargs):
        super(ulong, self).__init__(**kwargs)
        self._codebin = 0x4

        # Set default properties
        tmpdict = dict(self._defaultconfigs)
        tmpdict.update({
            'autoset': {
                'value': 1,
                'comment': True
            },
            'roundvalue': {
                'value': 10,
                'comment': True
            },
            'limit_crit': {
                'value': '> 90',
                'comment': True
            },
            'limit_warn': {
                'value': '>= 75',
                'comment': True
            },
            'limit_succ': {
                'value': '< 75',
                'comment': True
            }}
        )
        self._defaultconfigs = tmpdict

    @default.value.setter
    def value(self, value):
        if value:
            self._metadata['value'] = int(value)
        else:
            self._metadata['value'] = value

        self.checkMetadata()

    def typeToBinary(self):
        """Convert to Binary"""
        line = struct.pack('=BdL', self.codebin, self.time, self.value)
        return line

    def decodeBinary(self, content):
        """Binary to skline"""

        (sizes, typeid, datetime, value, sizee) = struct.unpack('=BBdLB', content)

        self.metadata['size'] = sizes
        self.metadata['time'] = datetime
        self.metadata['value'] = value

    def checkMetadata(self):
        super(ulong, self).checkMetadata()

        # Check value
        if not self.value:
            return

        if type(self.value) == str or type(self.value):
            self.metadata['value'] = int(self.value)

        if self.value >= 0 and self.value <= 65535:
            return

        raise Exception("Value %s not authorized in %s type" % (self.value, self.type))
