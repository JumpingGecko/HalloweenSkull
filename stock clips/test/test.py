from PIL import Image
import math

def convert(input, output):
    img = Image.open(input)

    x = img.width
    y = img.height
    scale = 240 / x
    xScale = int((x*scale) + 0.5)
    yScale = int((y*scale) + 0.5)

    img = img.resize((xScale,yScale))

    y_offset = 240 - yScale
    y_offset = int(y_offset / 2)

    new = Image.new('RGB', (240,240), (0,0,0))

    new.paste(img, (0, y_offset))
    new = new.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)
    new.save(output, 'JPEG')

def main():
    inPath = 'C:/Projects/HalloweenSkull/media/Eyes1/'
    outPath = 'C:/Projects/HalloweenSkull/media/Eyes1/right/'

    for i in range(1, 101):
        print("Processing Image %d..." % i)
        text = "-%03d.jpg" % i
        inFile = inPath + 'ezgif-frame' + text
        outFile = outPath + 'right' + text

        convert(inFile, outFile)

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
                         
if __name__ == '__main__':
    main()
    makeMergeImg()


