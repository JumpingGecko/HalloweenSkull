#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch28
from PIL import Image,ImageDraw,ImageFont

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)

def orig():
    try:
        # display with hardware SPI:
        ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
        #disp = LCD_1inch28.LCD_1inch28(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
        #disp1.Init()
        #disp1.clear()
        disp0 = LCD_1inch28.LCD_1inch28(0,0)
        disp1 = LCD_1inch28.LCD_1inch28(0,1)
        
        disp0.Init()
        disp0.clear()

        disp1.Init()
        disp1.clear()
        

        ################################
        image = Image.open('../pic/eyes.jpg')	
        img = disp0.np.asarray(image)
        pix = disp0.np.zeros((disp0.width,disp0.height,2), dtype = disp0.np.uint8)
        pix[...,[0]] = disp0.np.add(disp0.np.bitwise_and(img[...,[0]],0xF8),disp0.np.right_shift(img[...,[1]],5))
        pix[...,[1]] = disp0.np.add(disp0.np.bitwise_and(disp0.np.left_shift(img[...,[1]],3),0xE0),disp0.np.right_shift(img[...,[2]],3))
        pix = pix.flatten().tolist()
        disp0.SetWindows ( 0, 0, disp0.width, disp0.height)
        disp0.digital_write(disp0.DC_PIN, 1)

        st = time.time()
        frames = 100
        for i in range(0, frames):
            #im_r=image.rotate(i)
            #disp1.ShowImage(image)
            disp0.FastImage(pix)
        
        et = time.time()
        print("Start %f" % st)
        print("End %f" % et)
        diff = et - st
        print("diff %f" % (diff))
        print("FPS %f" % (frames / diff))
        
        sys.exit(0)
        
        ########################
        image = Image.open('../pic/eyes.jpg')	
        img = disp0.np.asarray(image)
        pix = disp0.np.zeros((disp0.width,disp0.height,2), dtype = disp0.np.uint8)
        
        st = time.time()
        frames = 100
        for i in range(0, frames):
            #im_r=image.rotate(i)
            #disp1.ShowImage(image)
            disp0.FastImage(img, pix)
        
        et = time.time()
        print("Start %f" % st)
        print("End %f" % et)
        diff = et - st
        print("diff %f" % (diff))
        print("FPS %f" % (frames / diff))
        
        disp0.module_exit()
        disp1.module_exit()
    except IOError as e:
        logging.info(e)    
    except KeyboardInterrupt:
        disp0.module_exit()
        logging.info("quit:")
        exit()

def loadImages(lcd, path, filePrefix):
    images = []
    
    #path = '/home/mpayne/Share/HalloweenSkull/media/Eyes1/left/'
    
    for i in range(1, 238):
        text = "%s-%03d.jpg" % (filePrefix, i)
        file = path + text
        image = Image.open(file)
        
        img = lcd.np.asarray(image)
        pix = lcd.np.zeros((lcd.width,lcd.height,2), dtype = lcd.np.uint8)
        pix[...,[0]] = lcd.np.add(lcd.np.bitwise_and(img[...,[0]],0xF8),lcd.np.right_shift(img[...,[1]],5))
        pix[...,[1]] = lcd.np.add(lcd.np.bitwise_and(lcd.np.left_shift(img[...,[1]],3),0xE0),lcd.np.right_shift(img[...,[2]],3))
        pix = pix.flatten().tolist()
        images.append(pix)

    return(images)
    
def main():
    left = LCD_1inch28.LCD_1inch28(0,0)
    left.Init()
    left.clear()
    
    # Calling this module_exit() and then re-running gets the
    # LCDs initialized correctly.  Need to investigate further.
    left.module_exit()
    left = LCD_1inch28.LCD_1inch28(0,0)
    left.Init()
    left.clear()
    
    right = LCD_1inch28.LCD_1inch28(0,1)
    right.Init()
    right.clear()
    
    print("Loading Images...")
    print("Left...")
    leftImages = loadImages(left, './media/Eye Balls 2/', 'eye')
    print("Done.")
    while (True):
        for z in range(0, 3):
            for i in range(0, len(leftImages)):
                #print("   Showing %d..." % i)
                left.FastImage(leftImages[i])
                right.FastImage(leftImages[i])
            for i in range(len(leftImages)-1, 0, -1):
                #print("   Showing %d..." % i)
                left.FastImage(leftImages[i])
                right.FastImage(leftImages[i])
        """
        print("Left...")
        leftImages = loadImages(left, '/home/mpayne/Share/HalloweenSkull/media/Eye Balls 1/Left/', 'left')
        print("Right...")
        rightImages = loadImages(right, '/home/mpayne/Share/HalloweenSkull/media/Eye Balls 1/Right/', 'right')
        print("Done.")
        for z in range(0, 3):
            for i in range(0, len(leftImages)):
                #print("   Showing %d..." % i)
                left.FastImage(leftImages[i])
                right.FastImage(rightImages[i])
            for i in range(len(leftImages)-1, 0, -1):
                #print("   Showing %d..." % i)
                left.FastImage(leftImages[i])
                right.FastImage(rightImages[i])

        leftImages = loadImages(left, '/home/mpayne/Share/HalloweenSkull/media/Fire Eyes/Left/', 'left')
        rightImages = loadImages(right, '/home/mpayne/Share/HalloweenSkull/media/Fire Eyes/Right/', 'right')
        for z in range(0, 3):
            for i in range(0, len(leftImages)):
                #print("   Showing %d..." % i)
                left.FastImage(leftImages[i])
                right.FastImage(rightImages[i])
            for i in range(len(leftImages)-1, 0, -1):
                #print("   Showing %d..." % i)
                left.FastImage(leftImages[i])
                right.FastImage(rightImages[i])
        """
        
def test():
    images = []
    
    p = '/home/mpayne/Share/HalloweenSkull/media/Eyes1/left/'
    
    for i in range(1, 101):
        text = "left-%03d.jpg" % i
        file = p + text
        #image = Image.open(file)
        image = Image.open('../pic/eyes.jpg')	
        images.append(image)
        
    disp0 = LCD_1inch28.LCD_1inch28(0,0)
    
    disp0.Init()
    disp0.clear()

    for i in range(0, len(images)):
        disp0.ShowImage(images[i])
       
if __name__ == '__main__':
    main()
    #test()