#! /usr/bin/env python

# Copyright (c) Ehab Aboudaya <ehab.abbyday@gmail.com> 2014
# All rights reserved.
#
# BSD-style license:
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY ehab aboudaya "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Albert Sweigart BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#   Respect to pyperclip.py license file

# Change Log:
# 0.1 inital version

# ToDo:
# check if notify osd installs and config is ok
# when calling show only it will not show last "only next" look at line 136

import os
import sys
import glob
import ConfigParser
import linecache
import string
import codecs
import pynotify
import pyperclip

def find_element_in_list(element,list_element):
        try:
            index_element=list_element.index(element)
            return index_element
        except ValueError:
            return -1

def updatesettings (updateposition):
    if changepos :
        config.set("General", "Currentfile", Currentfile)
        if updateposition:
            config.set("General", Currentfile, position)
        with open(settingsfilename, 'wb') as configfile:
            config.write(configfile)


def OnClicked(notification, signal_text):
    print '1: ' + str(notification)
    print '2: ' + str(signal_text)
    notification.close()
    global loop
    loop.quit()

def OnClosed(notification):
    print 'Ignoring fire'
    notification.close()
    global loop
    loop.quit()

def sendmessage(title, message):
    pynotify.init("Test")
    notice = pynotify.Notification(title, message)
    #notice.set_timeout(pynotify.EXPIRES_NEVER)
    notice.set_timeout(20 * 1000)
    #notice.add_action('You Clicked The Button', 'Remove Fire', OnClicked)
    #notice.connect("closed",OnClosed)
    notice.show()
    return


# we don't need to change position by passing any argument
changepos=(len(sys.argv)<=1)

# get the settinsg file
appdir=os.path.dirname(os.path.relpath(__file__));

# get the text file to display lines from
textdirs=appdir + "/textfiles/*.txt";
files=glob.glob(textdirs)

# read the settings file
settingsfilename=appdir + '/settings.ini'
config = ConfigParser.ConfigParser()
dataset = config.read(settingsfilename)
if len(dataset)==0:
	config.add_section("General")
	for f in files:
		config.set("General", f, 1)
	if len(files)>0:
		Currentfile=files[0];
		position=1;
else:
	try:
		Currentfile=config.get("General", "Currentfile");
		position=int(config.get("General", Currentfile));
	except ConfigParser.Error as e:
		print "Error parsing configuration: " + str (e)
		sys.exit(1)

condition=True;
beforesep="";
aftersep="";
line="";

while condition:
    textfilepos=find_element_in_list(Currentfile,files); # check if Currentfile exists
    if textfilepos == -1:
                        print "file :" + Currentfile + "\n not in settings list so exiting!"
                        #TODO :: update settings files and retain position
                        #config.remove_option("General", Currentfile)
                        #with open(settingsfilename, 'wb') as configfile:
                        #    config.write(configfile)
                        sys.exit(1)

    if os.path.getsize(Currentfile) == 0:
                        print "file :" + Currentfile + "\n size is 0 so exiting!"
                        sys.exit(1)
    err=False;
    try:
	line=config.get("General", "lastmsg");
	condition=False;
    except ConfigParser.Error as e:
	err=True
    if (changepos) or (err) or (len(line)==0):
		line=linecache.getline(Currentfile, position).strip('\n');
		if len(line):
			    condition=False;
			    # adavnce forward
			    position=position+1
			    config.set("General", "lastmsg", line)
			    updatesettings(True)
		else:
		    # update current file position
		    position=1  # line does not exists go back to line 1
		    config.set("General", "lastmsg", line)	    
		    updatesettings(True)
		linecache.clearcache();
#end of loop

try:
	material=line.split("|");
	beforesep=material[0]
	aftersep=material[1]
except:
	beforesep=os.path.basename(Currentfile);
	aftersep=line
	
# its time to show the popup	
sendmessage(beforesep ,aftersep);

if changepos :
	textfilepos=textfilepos+1
	if textfilepos >=len(files):
				    textfilepos=0
	Currentfile= files[textfilepos];
	updatesettings(False)
else:
	pyperclip.setcb(aftersep)




