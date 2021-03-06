###
# src/oled/python/server.py
###

import json
import subprocess
import threading
import time
import os
import sys
import base64

from io import BytesIO

import RPi.GPIO as GPIO
import OLED_Driver as OLED

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

## utility

def Display_Picture(File_Name):
    image = Image.open(File_Name)
    OLED.Display_Image(image)

## v1/test/ API

from flask import Flask, request, jsonify
webapp = Flask('oled')

###
### TESTING
###

@webapp.route("/oled/v1/test/text", methods=['GET'])
def Test_Text():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('cambriab.ttf',24)

    draw.text((0, 12), 'WaveShare', fill = "BLUE", font = font)
    draw.text((0, 36), 'Electronic', fill = "BLUE",font = font)
    draw.text((20, 72), '1.5 inch', fill = "CYAN", font = font)
    draw.text((10, 96), 'R', fill = "RED", font = font)
    draw.text((25, 96), 'G', fill = "GREEN", font = font)
    draw.text((40, 96), 'B', fill = "BLUE", font = font)
    draw.text((55, 96), ' OLED', fill = "CYAN", font = font)

    OLED.Display_Image(image)
    return ('{"success": true}\n' % ())

def testPattern():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    draw.line([(0,8), (127,8)],   fill = "RED",    width = 16)
    draw.line([(0,24),(127,24)],  fill = "YELLOW", width = 16)
    draw.line([(0,40),(127,40)],  fill = "GREEN",  width = 16)
    draw.line([(0,56),(127,56)],  fill = "CYAN",   width = 16)
    draw.line([(0,72),(127,72)],  fill = "BLUE",   width = 16)
    draw.line([(0,88),(127,88)],  fill = "MAGENTA",width = 16)
    draw.line([(0,104),(127,104)],fill = "BLACK",  width = 16)
    draw.line([(0,120),(127,120)],fill = "WHITE",  width = 16)
    OLED.Display_Image(image)

@webapp.route("/oled/v1/test/pattern", methods=['GET'])
def Test_Pattern():
    testPattern()
    return ('{"success": true}\n' % ())

@webapp.route("/oled/v1/test/lines", methods=['GET'])
def Test_Lines():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)

    for x in range(0, int((OLED.SSD1351_WIDTH-1)/2), 6):
        draw.line([(0, 0), (x, OLED.SSD1351_HEIGHT - 1)], fill = "RED", width = 1)
        draw.line([(0, 0), ((OLED.SSD1351_WIDTH-1) - x, OLED.SSD1351_HEIGHT - 1)], fill = "RED", width = 1)
        draw.line([(0, 0), (OLED.SSD1351_WIDTH - 1, x)], fill = "RED", width = 1)
        draw.line([(0, 0), (OLED.SSD1351_WIDTH - 1, (OLED.SSD1351_HEIGHT-1) - x)], fill = "RED", width = 1)
        OLED.Display_Image(image)
    OLED.Delay(250)
    draw.rectangle([0, 0, OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1], fill = "BLACK", outline = "BLACK")

    for x in range(0, int((OLED.SSD1351_WIDTH-1)/2), 6):
        draw.line([(OLED.SSD1351_WIDTH - 1, 0), (x, OLED.SSD1351_HEIGHT - 1)], fill = "YELLOW", width = 1)
        draw.line([(OLED.SSD1351_WIDTH - 1, 0), (x + int((OLED.SSD1351_WIDTH-1)/2), OLED.SSD1351_HEIGHT - 1)], fill = "YELLOW", width = 1)
        draw.line([(OLED.SSD1351_WIDTH - 1, 0), (0, x)], fill = "YELLOW", width = 1)
        draw.line([(OLED.SSD1351_WIDTH - 1, 0), (0, x + int((OLED.SSD1351_HEIGHT-1)/2))], fill = "YELLOW", width = 1)
        OLED.Display_Image(image)
    OLED.Delay(250)
    draw.rectangle([0, 0, OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1], fill = "BLACK", outline = "BLACK")

    for x in range(0, int((OLED.SSD1351_WIDTH-1)/2), 6):
        draw.line([(0, OLED.SSD1351_HEIGHT - 1), (x, 0)], fill = "BLUE", width = 1)
        draw.line([(0, OLED.SSD1351_HEIGHT - 1), (x + int((OLED.SSD1351_WIDTH-1)/2), 0)], fill = "BLUE", width = 1)
        draw.line([(0, OLED.SSD1351_HEIGHT - 1), (OLED.SSD1351_WIDTH - 1, x)], fill = "BLUE", width = 1)
        draw.line([(0, OLED.SSD1351_HEIGHT - 1), (OLED.SSD1351_WIDTH - 1, x + (OLED.SSD1351_HEIGHT-1)/2)], fill = "BLUE", width = 1)
        OLED.Display_Image(image)
    draw.rectangle([0, 0, OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1], fill = "BLACK", outline = "BLACK")
    OLED.Delay(250)
    
    for x in range(0, int((OLED.SSD1351_WIDTH-1)/2), 6):
        draw.line([(OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1), (x, 0)], fill = "GREEN", width = 1)
        draw.line([(OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1), (x + int((OLED.SSD1351_WIDTH-1)/2), 0)], fill = "GREEN", width = 1)
        draw.line([(OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1), (0, x)], fill = "GREEN", width = 1)
        draw.line([(OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1), (0, x + int((OLED.SSD1351_HEIGHT-1)/2))], fill = "GREEN", width = 1)
        OLED.Display_Image(image)
    draw.rectangle([0, 0, OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1], fill = "BLACK")
    return ('{"success": true}\n' % ())

@webapp.route("/oled/v1/test/hv-lines", methods=['GET'])
def Test_HV_Lines():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    
    for y in range(0, OLED.SSD1351_HEIGHT - 1, 5):
        draw.line([(0, y), (OLED.SSD1351_WIDTH - 1, y)], fill = "WHITE", width = 1)
    OLED.Display_Image(image)
    OLED.Delay(250)
    for x in range(0, OLED.SSD1351_WIDTH - 1, 5):
        draw.line([(x, 0), (x, OLED.SSD1351_HEIGHT - 1)], fill = "WHITE", width = 1)
    OLED.Display_Image(image)
    return ('{"success": true}\n' % ())

@webapp.route("/oled/v1/test/rects", methods=['GET'])
def Test_Rects():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    
    for x in range(0, int((OLED.SSD1351_WIDTH-1)/2), 6):
        draw.rectangle([(x, x), (OLED.SSD1351_WIDTH- 1 - x, OLED.SSD1351_HEIGHT-1 - x)], fill = None, outline = "WHITE")
    OLED.Display_Image(image)
    return ('{"success": true}\n' % ())

@webapp.route("/oled/v1/test/fillrects", methods=['GET'])
def Test_FillRects(): 
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    
    for x in range(OLED.SSD1351_HEIGHT-1, int((OLED.SSD1351_HEIGHT-1)/2), -6):
        draw.rectangle([(x, x), ((OLED.SSD1351_WIDTH-1) - x, (OLED.SSD1351_HEIGHT-1) - x)], fill = "BLUE", outline = "BLUE")
        draw.rectangle([(x, x), ((OLED.SSD1351_WIDTH-1) - x, (OLED.SSD1351_HEIGHT-1) - x)], fill = None, outline = "YELLOW")
    OLED.Display_Image(image)
    return ('{"success": true}\n' % ())

@webapp.route("/oled/v1/test/circles", methods=['GET'])
def Test_Circles():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)

    draw.ellipse([(0, 0), (OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1)], fill = "BLUE", outline = "BLUE")
    OLED.Display_Image(image)
    OLED.Delay(500)
    for r in range(0, int(OLED.SSD1351_WIDTH/2) + 4, 4):
        draw.ellipse([(r, r), ((OLED.SSD1351_WIDTH-1) - r, (OLED.SSD1351_HEIGHT-1) - r)], fill = None, outline = "YELLOW")
    OLED.Display_Image(image)
    return ('{"success": true}\n' % ())

@webapp.route("/oled/v1/test/triangles", methods=['GET'])
def Test_Triangles():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    
    for i in range(0, int(OLED.SSD1351_WIDTH/2), 4):
        draw.line([(i, OLED.SSD1351_HEIGHT - 1 - i), (OLED.SSD1351_WIDTH/2, i)], fill = (255 - i*4, i*4, 255 - i*4), width = 1)
        draw.line([(i, OLED.SSD1351_HEIGHT - 1 - i), (OLED.SSD1351_WIDTH - 1 - i, OLED.SSD1351_HEIGHT - 1 - i)], fill = (i*4, i*4 ,255 - i*4), width = 1)
        draw.line([(OLED.SSD1351_WIDTH - 1 - i, OLED.SSD1351_HEIGHT - 1 - i), (OLED.SSD1351_WIDTH/2, i)], fill = (i*4, 255 - i*4, i*4), width = 1)
        OLED.Display_Image(image)
    return ('{"success": true}\n' % ())

@webapp.route("/oled/v1/test/picture", methods=['GET'])
def Test_Picture():
  Display_Picture("picture1.jpg")
  Display_Picture("picture2.jpg")
  Display_Picture("picture3.jpg")
  Display_Picture("picture4.jpg")
  return ('{"success": true}}\n' % ())

###
### OLED functions
###

## LIBRARY

# display image on SPI OLED display
def displayImage(b64data):
  imageBytes = base64.b64decode(b64data)
  if imageBytes != 'null':
    stream = BytesIO(imageBytes)
    if stream != 'null':
      image = Image.open(stream).convert("RGBA")
      if image != 'null':
        imageSmall = image.resize((128, 128), Image.ANTIALIAS)
        if imageSmall != 'null':
          OLED.Display_Image(imageSmall)
          return 'true'
        else:
          return null
      else:
        return null
    else:
      return null
  else:
    return null

# clean the I2C display
def clearEvent():
  line1 = 'EVENT'
  line2 = 'ENTITY'
  line3 = 'COUNT'
  command = './i2c/oled ' + json.dumps(line1) + ' ' + json.dumps(line2) + ' ' + json.dumps(line3)
  os.system(command)
  return 'true'

# display event information on the I2C display
def displayEvent(payload):
  line1 = 'NO EVENT'
  line2 = 'NO ENTITY'
  line3 = 'NOTHING'
  event = payload['event']
  if event != 'null':
    group = event['group']
    device = event['device']
    camera = event['camera']
    line1 = str(camera)
  detected = payload['detected']
  if detected is not None and len(detected) > 0:
    person = 'null'
    for sub in detected:
      if sub['entity'] == 'person':
        person = sub
        break
    if person != 'null':
      number = person['count']
      line2 = 'person(s): ' + str(number)
  count = payload['count']
  if count != 'null' and int(count) > 0:
    line3 = 'total: ' + str(count)
  command = './i2c/oled ' + json.dumps(line1) + ' ' + json.dumps(line2) + ' ' + json.dumps(line3)
  os.system(command)
  return 'true'

## API

# display annotated event on both SPI and I2C OLED displays
@webapp.route("/oled/v1/display/annotated", methods=['POST'])
def displayAnnotated():
  json_data = request.get_json(force=True)
  if json_data != 'null':
    result = displayEvent(json_data)
    if result != 'null':
      b64data = json_data['image']
      if b64data != 'null':
        result = displayImage(b64data)
        if result != 'true':
          return ('{"error": "failed to displayImage"}\n' % ())
        else:
          return ('{"success": true}\n' % ())
      else:
        return ('{"error": "No BASE64 data"}\n' % ())
    else:
      return ('{"error": "failed to displayEvent"}\n' % ())
  else:
    return ('{"error": "No JSON data"}\n' % ())

###
###
### MAIN
###

try:
  if __name__ == '__main__':
    narg = len(sys.argv)
    if narg > 1:
      arg1 = sys.argv[1]
    else:
      arg1=os.environ("OLED_HOST")
    if len(arg1) < 1:
      arg1 = "127.0.0.1"
    if narg > 2:
      arg2 = sys.argv[2]
    else:
      arg2=os.environ("OLED_PORT")
    if len(arg2) < 1:
      arg2=7777
    OLED.Device_Init()
    OLED.Clear_Screen()
    testPattern()
    OLED.Clear_Screen()
    clearEvent()
    webapp.run(debug=True,host=arg1,port=arg2)

except:
  OLED.Clear_Screen()
  GPIO.cleanup()
