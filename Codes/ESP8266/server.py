#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  server.py
#  
#  Copyright 2018 Michael <michael@UMO-PC5>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


import socket
import machine
import time



#HTML to send to browsers
html = """<!DOCTYPE html>
<html>
<meta name="viewport" content="width=device-width, initial-scale=1.0"> 
<form>
DOOR:
<button name="room" value="unlock" type="submit">UNLOCK</button>
<button name="room" value="lock" type="submit">LOCK</button><br><br>
</form>
"""
sub = """
</html>
"""

#Setup PINS
servo = machine.PWM(machine.Pin(2), freq=50)
pin = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)


#Setup Socket WebServer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
error = 0

while error == False:
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    request = conn.recv(1024)
    print("Content = %s" % str(request))
    request = str(request)
    lock = request.find('/?room=lock')
    unlock = request.find('/?room=unlock')
    if pin.value() == True:
		if lock == 6:
			servo.duty(40)
		if unlock == 6:
			servo.duty(77)
		time.sleep_ms(1500)
		servo.duty(0)
		conn.send(html+sub)
    else :
		conn.send(html+"battery power low!!"+sub)
		error = 1
    conn.close()
