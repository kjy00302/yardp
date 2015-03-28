#!/usr/bin/python
# -*- coding: UTF-8 -*-
import hiddict, re, time, string, StringIO, argparse, sys

parser = argparse.ArgumentParser(description='Yet Another USB Rubber Ducky Parser.\nDefault HID Gadget device is "/dev/hidg0".', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-d', type=str, dest='hiddev', default="/dev/hidg0", help='HID Gadget device')
parser.add_argument('duckyscript',type=file)

try:
 args = parser.parse_args()
except IOError:
 sys.exit("Can't open Duckyscript!")

locale = "us"
defaultsleep = 0
script = args.duckyscript

try:
 hiddev = open (args.hiddev, "w")
except IOError:
 sys.exit("Can't open HID Gadget device!\nPlease run as root!")

arg1 =re.compile('(^[a-zA-Z0-9\-]*)\s?(.*)')
arg2 =re.compile('(^\w*)\s?(\w*)\s?(\w*)\s?(\w*)\s?(\w*)\s?(\w*)')
repeated = 0
repeat = 0
inrepeat = False

def presskey(mod, a, b, c, d, e, f): 
 if a == "" :
  a = "\00"
 else:
  a = hiddict.findinlist(a, "singlekey")

 if b == "" :
  b = "\00"
 else:
  b = hiddict.findinlist(b, "singlekey")

 if c == "" :
  c = "\00"
 else:
  c = hiddict.findinlist(c, "singlekey")
  
 if d == "" :
  d = "\00"
 else:
  d = hiddict.findinlist(d, "singlekey")
  
 if e == "" :
  e = "\00"
 else:
  e = hiddict.findinlist(e, "singlekey")
  
 if f == "" :
  f = "\00"
 else:
  f = hiddict.findinlist(f,  "singlekey")
 hiddev.write(mod+"\00"+a+b+c+d+e+f)
 hiddev.write("\x00\x00\x00\x00\x00\x00\x00\x00")
 
def duckscan():
 global parsingline
 global defaultsleep
 global inrepeat
 global repeated
 global repeat
 m = arg1.search(parsingline)
 if m.group(1) == "REM":
  pass
 elif m.group(1) =="DELAY":
  time.sleep(0.001*string.atoi(m.group(2)))
 elif (m.group(1) == "DEFAULT_DELAY") or (m.group(1) == "DEFAULTDELAY"):
  defaultsleep = string.atoi(m.group(2))
 elif m.group(1) == "STRING":
  l = StringIO.StringIO(m.group(2))
  byte = l.read(1)
  while byte != "":
   if byte:
    hiddev.write(hiddict.findinlist(byte, locale))
    hiddev.write("\x00\x00\x00\x00\x00\x00\x00\x00")
    time.sleep(defaultsleep*0.001)
   byte = l.read(1)
 elif m.group(1) == "ENTER":
  keys = arg2.search(m.group(2))
  presskey("\x00", "ENTER", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif (m.group(1) == "GUI") or (m.group(1) == "WINDOWS"):
  keys = arg2.search(m.group(2))
  presskey("\x08", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5), keys.group(6))
 elif (m.group(1) == "MENU") or (m.group(1) == "APP"):
  keys = arg2.search(m.group(2))
  presskey("\x00", "MENU", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "SHIFT":
  keys = arg2.search(m.group(2))
  presskey("\x02", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5), keys.group(6))
 elif m.group(1) == "ALT":
  keys = arg2.search(m.group(2))
  presskey("\x04", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5), keys.group(6))
 elif (m.group(1) == "CONTROL") or (m.group(1) == "CTRL"):
  keys = arg2.search(m.group(2))
  presskey("\x01", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5), keys.group(6))
 elif m.group(1) == "CTRL-ALT":
  keys = arg2.search(m.group(2))
  presskey("\x05", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5), keys.group(6))
 elif m.group(1) == "CTRL-SHIFT":
  keys = arg2.search(m.group(2))
  presskey("\03", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5), keys.group(6))
 elif m.group(1) == "ALT-SHIFT":
  keys = arg2.search(m.group(2))
  presskey("\06", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5), keys.group(6))
 elif (m.group(1) == "DOWNARRORW") or (m.group(1) == "DOWN"):
  keys = arg2.search(m.group(2))
  presskey("\x00", "DOWN", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif (m.group(1) == "LEFTARRORW") or (m.group(1) == "LEFT"):
  keys = arg2.search(m.group(2))
  presskey("\x00", "LEFT", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif (m.group(1) == "RIGHTARRORW") or (m.group(1) == "RIGHT"):
  keys = arg2.search(m.group(2))
  presskey("\x00", "RIGHT", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif (m.group(1) == "UPARRORW") or (m.group(1) == "UP"):
  keys = arg2.search(m.group(2))
  presskey("\x00", "UP", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif (m.group(1) == "BREAK") or (m.group(1) == "PAUSE"):
  keys = arg2.search(m.group(2))
  presskey("\x00", "BREAK", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "CAPSLOCK":
  keys = arg2.search(m.group(2))
  presskey("\x00", "CAPSLOCK", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "DELETE":
  keys = arg2.search(m.group(2))
  presskey("\x00", "DELETE", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "END":
  keys = arg2.search(m.group(2))
  presskey("\x00", "END", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif (m.group(1) == "ESC") or (m.group(1) == "ESCAPE"):
  keys = arg2.search(m.group(2))
  presskey("\x00", "ESC", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "HOME":
  keys = arg2.search(m.group(2))
  presskey("\x00", "HOME", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "INSERT":
  keys = arg2.search(m.group(2))
  presskey("\x00", "INSERT", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "NUMLOCK":
  keys = arg2.search(m.group(2))
  presskey("\x00", "NUMLOCK", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "PAGEUP":
  keys = arg2.search(m.group(2))
  presskey("\x00", "PAGEUP", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "PAGEDOWN":
  keys = arg2.search(m.group(2))
  presskey("\x00", "PAGEDOWN", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "PRINTSCREEN":
  keys = arg2.search(m.group(2))
  presskey("\x00", "PRINTSCREEN", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "SCROLLLOCK":
  keys = arg2.search(m.group(2))
  presskey("\x00", "SCROLLLOCK", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "SPACE":
  keys = arg2.search(m.group(2))
  presskey("\x00", "SPACE", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "TAB":
  keys = arg2.search(m.group(2))
  presskey("\x00", "TAB", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "F1":
  keys = arg2.search(m.group(2))
  presskey("\x00", "F1", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "F2":
  keys = arg2.search(m.group(2))
  presskey("\x00", "F2", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "F3":
  keys = arg2.search(m.group(2))
  presskey("\x00", "F3", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "F4":
  keys = arg2.search(m.group(2))
  presskey("\x00", "F4", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "F5":
  keys = arg2.search(m.group(2))
  presskey("\x00", "F5", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "F6":
  keys = arg2.search(m.group(2))
  presskey("\x00", "F6", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "F7":
  keys = arg2.search(m.group(2))
  presskey("\x00", "F7", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "F8":
  keys = arg2.search(m.group(2))
  presskey("\x00", "F8", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "F9":
  keys = arg2.search(m.group(2))
  presskey("\x00", "F9", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "F10":
  keys = arg2.search(m.group(2))
  presskey("\x00", "F10", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "F11":
  keys = arg2.search(m.group(2))
  presskey("\x00", "F11", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif m.group(1) == "F12":
  keys = arg2.search(m.group(2))
  presskey("\x00", "F12", keys.group(1), keys.group(2), keys.group(3), keys.group(4), keys.group(5))
 elif (m.group(1) == "REPEAT") and (inrepeat == False):
  repeat = string.atoi(m.group(2))
  inrepeat = True
  while repeated < repeat:
   parsingline = lastline
   duckscan()
   repeated = repeated +1
  inrepeat = False

parsingline= script.readline() 
try:
 while parsingline != "" :
  duckscan()
  time.sleep(defaultsleep*0.001)
  lastline = parsingline
  parsingline= script.readline() 
except KeyboardInterrupt:
 print("\nKeyboard Interrupt\nstopping..")
 hiddev.write("\x00\x00\x00\x00\x00\x00\x00\x00")
script.close
hiddev.close