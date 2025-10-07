from PIL import Image
import math
import glob
import os
import sys

def main_old():
    img = Image.open(r"image1.jpg")
    merge = Image.open(r"merge2.jpg")

    x = img.width
    y = img.height
    scale = 240 / x
    xScale = int((x*scale) + 0.5)
    yScale = int((y*scale) + 0.5)

    img = img.resize((xScale,yScale))

    row = []
    for i in range(0, 240):
        px = img.getpixel((i,0))
        row.append(px)

    y_offset = 240 - yScale
    y_offset = int(y_offset / 2)

    new = Image.new('RGB', (240,240), (255,255,255))

    for i in range(0, 240):
        for j in range(0, y_offset):
            new.putpixel((i,j), row[i])

    new = Image.blend(new, merge, 0.25)
    new.save('check.jpg', 'JPEG')

    new.paste(img, (0, y_offset))

    new.save('new.jpg', 'JPEG')

def makeMergeImg():
    img = Image.new('RGB', (240, 240), (255,255,255))
    cx = 120
    cy = 120

    for x in range(0, 240):
        for y in range(0, 240):
            dx = abs(x - cx)
            dy = abs(y - cy)
            f = math.sqrt((dx*dx) + (dy*dy))
            c = int(120 - f)
            if (c < 0):
                c = 0
            img.putpixel((x,y), (c,c,c))

    img.save('merge2.jpg', 'JPEG')
            
class cStock():
    def __init__(self, folder, xStart, xEnd):
        self.folder = folder
        self.xCropStart = xStart
        self.xCropEnd = xEnd
      
        self.inputFolder = "../clips/" + self.folder
        list = glob.glob(self.inputFolder + '/*.jpg')
        self.files = []
        for file in list:
            self.files.append(os.path.basename(file))
            
        self.outputFolder = "../../media/" + self.folder
        if (os.path.isdir(self.outputFolder) == False):
            os.mkdir(self.outputFolder)
            
    def openImage(self, filename):
        path = self.inputFolder + '/' + filename
        handle = Image.open(path)
        
        return(handle)
        
    def processImage(self, filename):
        img = self.openImage(filename)
        xSize = img.width
        ySize = img.height

        # Crop out the image we want to start with
        eye = Image.new('RGB', (self.xCropEnd - self.xCropStart, ySize), (255,255,255))
        for y in range(0, ySize):
            for x in range(self.xCropStart, self.xCropEnd):
                px = img.getpixel((x, y))
                eye.putpixel((x-self.xCropStart, y), px)

        # Now scale it
        
        # Calculate the scale factors
        xSize = self.xCropEnd - self.xCropStart
        scale = 240 / xSize
        xScale = int((xSize*scale) + 0.5)
        yScale = int((ySize*scale) + 0.5)

        # Scale the image while maintaining
        # the aspect ratio
        eye = eye.resize((xScale,yScale))
        
        # Create a new image that we'll paste into
        xSize = eye.width
        ySize = eye.height
        new = Image.new('RGB', (240,240), (64,64,64))
        new.paste(eye, (0, int((240-ySize)/2)),None)
        
        new = new.rotate(angle=180)
        new = new.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)
        for y in range(0, 240):
            for x in range(0, 240):
                px = new.getpixel((x,y))
                px = (px[2], px[1], px[0])
                new.putpixel((x,y), px)
                
        filename = filename.replace('ezgif-frame', 'right')
        new.save(self.outputFolder + '/' + filename)
        
def main_last_last():
    media1 = cStock('Fire Eyes', 58, 424)
    for file in media1.files:
        print("Processing %s..." % file)
        media1.processImage(file)
        
       
        
def last_main():
    p = "../Eyes 2/"
    
    img = Image.open(p + "ezgif-frame-001.jpg")
    xSize = img.width
    ySize = img.height

    xCropStart = 58
    xCropEnd = 424
    
    eye = Image.new('RGB', (xCropEnd - xCropStart, ySize), (255,255,255))
    for y in range(0, ySize):
        for x in range(xCropStart, xCropEnd):
            px = img.getpixel((x, y))
            eye.putpixel((x-xCropStart, y), px)

    xSize = xCropEnd - xCropStart
    scale = 240 / xSize
    xScale = int((xSize*scale) + 0.5)
    yScale = int((ySize*scale) + 0.5)

    eye = eye.resize((xScale,yScale))
    
    xSize = eye.width
    ySize = eye.height
    new = Image.new('RGB', (240,240), (255,255,255))
    new.paste(eye, (0, int((240-ySize)/2)),None)
    
    new.save(p + "test.jpg")

class cStock2():
    def __init__(self, folder):
        self.folder = folder
        self.xLeft = 335
        self.yLeft = 60
        
        self.xRight = 355
        self.yRight = 110
        
        self.xSize = 630
        self.ySize = 630
        
        self.inputFolder = "../clips/" + self.folder
        list = glob.glob(self.inputFolder + '/*.jpg')
        self.files = []
        for file in list:
            self.files.append(os.path.basename(file))
            
        self.outputFolder = "../../media/" + self.folder
        if (os.path.isdir(self.outputFolder) == False):
            os.mkdir(self.outputFolder)
            os.mkdir(self.outputFolder + '/Left')
            os.mkdir(self.outputFolder + '/Right')
            
    def openImage(self, filename):
        path = self.inputFolder + '/' + filename
        handle = Image.open(path)
        
        return(handle)
        
    def getLeft(self, img):
        lImg = img.crop((self.xLeft, self.yLeft, self.xLeft + self.xSize, self.yLeft + self.ySize))
        return(lImg)
        
    def getRight(self, img):
        rImg = img.crop((self.xRight, self.yRight, self.xRight + self.xSize, self.yRight + self.ySize))
        return(rImg)
        
    def processImage(self, filename):
        img = self.openImage(filename)

        new = self.getLeft(img)
        
        cx = 630 / 2
        cy = 630 / 2
        for y in range(0, 630):
            for x in range(0, 630):
                px = new.getpixel((x,y))
                px = (px[2], px[1], px[0])
                dx = abs(x - cx)
                dy = abs(y - cy)
                R = math.sqrt((dx*dx) + (dy*dy))
                if (R > 630/2):
                    px = (0,0,0)
                new.putpixel((x,y), px)
                
        eye = new.resize((240, 240))
        eye = eye.rotate(angle=180)
        
        filename = filename[-7:]
        Filename = 'eye-' + filename
        eye.save(self.outputFolder + '/' + Filename)
    
def main():
    media1 = cStock2('Eye Balls 2')
    for file in media1.files:
        print("Processing %s..." % file)
        media1.processImage(file)
        
if __name__ == '__main__':
    main()


