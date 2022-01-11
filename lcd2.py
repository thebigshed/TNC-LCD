from binascii import a2b_hex
from struct import unpack
import socket as python_socket
from pathlib import Path
import datetime
import calendar
import socket
import dateutil.parser as dparser
import numpy as np
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
lcd = LCD()

mtype = [('Call','S12'), ('Packets',int),('Date', 'S19')]
ta = np.zeros((0), dtype=mtype)

def from_hex(hexstr):
    return a2b_hex(hexstr.replace(' ', ''))

def to_hex(bytestr):
    return ' '.join([
        '%02x' % byte
        for byte in bytestr
    ])

def decode(data):
    if isinstance(data, (bytes, bytearray)):
        # Ensure the data is at least 7 bytes!
        if len(data) < 7:
            raise ValueError('AX.25 addresses must be 7 bytes!')

        # This is a binary representation in the AX.25 frame header
        callsign = bytes([
            b >> 1
            for b in data[0:6]
        ]).decode('US-ASCII').strip()
        ssid = (data[6] & 0b00011110) >> 1
        ch = bool(data[6] & 0b10000000)
        res1 = bool(data[6] & 0b01000000)
        res0 = bool(data[6] & 0b00100000)
        extension = bool(data[6] & 0b00000001)
    if ssid > 0:
        callsign = callsign + "-" + str(ssid)
    return callsign

file_name = '/var/ax25/mheard/mheard.dat'
num_bytes = Path(file_name).stat().st_size * 2

with open(file_name, 'rb') as f:
    hex_addr = f.read().hex()
    
n = 0
packet_offset = 72
offset =232

while n < num_bytes:
    hexlist = hex_addr[n] + hex_addr[n+1] + " " + hex_addr[n+2] + hex_addr[n+3] + " " + hex_addr[n+4] + hex_addr[n+5] + " " + hex_addr[n+6] + \
        hex_addr[n+7] + " " + hex_addr[n+8] + hex_addr[n+9] + " " + \
        hex_addr[n+10] + hex_addr[n+11] + " " + hex_addr[n+12] + hex_addr[n+13]
    addr = decode(from_hex(hexlist))
    addr = (addr.ljust(12)).ljust(15)
    packets = hex_addr[n+packet_offset+2] + hex_addr[n+packet_offset +
                                                     3] + hex_addr[n+packet_offset] + hex_addr[n+packet_offset+1]
    
    last_heard_hex = hex_addr[n+offset+6] + hex_addr[n+offset + 7] + hex_addr[n+offset+4] + hex_addr[n+offset+5]+hex_addr[n+offset+2] + hex_addr[n+offset + 3] + hex_addr[n+offset+0] + hex_addr[n+offset+1]
    last_heard_hex = "0x"+last_heard_hex                                                 
      
    recovernow = datetime.datetime.fromtimestamp(int(last_heard_hex,16))
    ta = np.append(ta, np.array([(str(addr), '{0:06}'.format(int(packets, 16)), recovernow)], dtype=mtype))
    n = n+512

ta.sort(order='Date')

for line in range(1,4):
    temp = str(ta[0-line])
    x=temp.find(":")
    call_txt = temp[3:12] + "   " + temp[(x-2):(x+6)]
    lcd.text(call_txt, line)


lcd.text("TNC2 " + socket.gethostbyname(socket.gethostname()),4)
