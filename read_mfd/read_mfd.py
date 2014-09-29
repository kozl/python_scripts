#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 14:07:18 2014

@author: q
"""

from binascii import hexlify
from datetime import datetime, timedelta
import sys
import struct

DATE_ZERO = datetime(1992, 01, 01)

mf_ultralight = struct.Struct('9s 1s 2s 4s 48s')
binary = lambda x: " ".join(reversed( [i+j for i,j in zip( *[ ["{0:04b}".format(int(c,16)) for c in reversed("0"+x)][n::2] for n in [1,0] ] ) ] ))
hexademal = lambda x: " ".join([x[a:a+2] for a in range(0,len(x)-1,2)]).upper()

def decode_metro(user_data):
    decoded = {}
    decoded['app_id'] = int(user_data[0:5],16) & 0xffc00
    decoded['card_type'] = int(user_data[0:5],16) & 0x003ff
    decoded['card_number'] = int(user_data[5:13],16)
    decoded['layout'] = int(user_data[13],16)
    decoded['unknown1'] = hexademal(user_data[14:32])
    decoded['date_created'] = DATE_ZERO+timedelta(days=int(user_data[32:36],16))
    decoded['duration'] = int(user_data[36:38],16)
    decoded['unknown2'] = hexademal(user_data[38:42])
    decoded['trips'] = int(user_data[42:44],16)
    decoded['turn_id'] = int(user_data[44:48],16)
    decoded['crc'] = hexademal(user_data[48:56])
    decoded['date_modified'] = DATE_ZERO+timedelta(days=int(user_data[56:60],16))
    decoded['unknown3'] = hexademal(user_data[60:64])
    return decoded

for infile in sys.argv[1:]:    
    mfd_file = open(infile,'rb')
    filename = infile
    data = mf_ultralight.unpack(mfd_file.read())
    data = [ hexlify(item) for item in data ]
    decoded = decode_metro(data[-1])    
    text = '''Filename: {0}
    
SERIAL_NUMBER:      {1}
INTERNAL:           {2}
LOCK BYTES:         {3}
OTP:                {4}
    
USER DATA:          
    
{5}
------------------------------------

DECODED:
--------
Идентификатор приложения:             {app_id:d}
Тип карты:                            {card_type:d}
Номер карты:                          {card_number:d}
Layout:                               {layout:d}
НЕИЗВЕСТНО:                           {unknown1}

Дата создания:                        {date_created:%d.%m.%Y}
НЕИЗВЕСТНО:                           {unknown2}
Срок действия:                        {duration:d}
Количество поездок:                   {trips:d}
Номер турникета:                      {turn_id:d}
Контрольная сумма:                    {crc}
Дата прохода:                         {date_modified}
НЕИЗВЕСТНО:                           {unknown3}
=============================================================
'''
    
    print text.format(filename, \
                      hexademal(data[0]), \
                      hexademal(data[1]), \
                      binary(data[2]), \
                      binary(data[3]), \
                      hexademal(data[4]), \
                      **decoded)
