# Copyright (C) 2015 Real Time Enterprises, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
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
