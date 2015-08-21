# Copyright (c) 2015, Robert Tanner <tanner@real-time.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this
# list of conditions and the following disclaimer in the documentation and/or other
# materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
# OF SUCH DAMAGE.
#
from nose import with_setup
from nose.tools import raises
import ConfigParser, os
from PyFileMaker import FMServer

class TestFMServer:
    
    def setUp(self):
        config = ConfigParser.ConfigParser()
#        config.readfp(open('mytesting.cfg'))
#        
#        self.hostname = config.get('testing', 'hostname')
#        self.username = config.get('testing', 'username')
#        self.password = config.get('testing', 'password')
#        
#        self.databases = config.get('testing', 'databases').split(',')
#        self.databases = [x.strip(' ') for x in self.databases]
#        
#        self.layout = config.get('testing', 'layout')
#        
#        self.fm = CheckFilemaker()
#        self.fm.connect(self.hostname, self.username, self.password, self.databases[0], self.layout)
            
    def tearDown(self):
        pass
       
    def test_1(self):
        """Test hostnames with dashes"""
        FMServer('login:password@filemaker-1.server.com')
        FMServer('login:password@filemaker-1-2.server.com')
        FMServer('login:password@f-i-l-e-m-a-k-e-r-1-2.server.com')
