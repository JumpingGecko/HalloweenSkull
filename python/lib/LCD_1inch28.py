
import time
from . import lcdconfig

class LCD_1inch28(lcdconfig.RaspberryPi):

    width = 240
    height = 240 
    def __init__(self, bus=0, device=0):
        super().__init__(spiBus=bus, spiDevice=device)

    def command(self, cmd):
        self.digital_write(self.DC_PIN, LCD_1inch28.global_GPIO.LOW)
        self.spi_writebyte([cmd])
        
    def data(self, list):
        self.digital_write(self.DC_PIN, LCD_1inch28.global_GPIO.HIGH)
        self.spi_writebyte([list])
        
    def reset(self):
        """Reset the display"""
        LCD_1inch28.global_GPIO.output(self.RST_PIN, LCD_1inch28.global_GPIO.HIGH)
        time.sleep(0.01)
        LCD_1inch28.global_GPIO.output(self.RST_PIN, LCD_1inch28.global_GPIO.LOW)
        time.sleep(0.01)
        LCD_1inch28.global_GPIO.output(self.RST_PIN, LCD_1inch28.global_GPIO.HIGH)
        time.sleep(0.01)
        
    def _write(self, command=None, data=None):
        """SPI write to the device: commands and data."""

        if command is not None:
            self.command(command)
            
        if data is not None:
            self.digital_write(self.DC_PIN, LCD_1inch28.global_GPIO.HIGH)
            self.spi_writebyte(data)

    def Init(self):
        time.sleep(0.100)

        self._write(0xEF)
        self._write(0xEB, [0x14])
        self._write(0xFE)
        self._write(0xEF)
        self._write(0xEB, [0x14])
        self._write(0x84, [0x40])
        self._write(0x85, [0xFF])
        self._write(0x86, [0xFF])
        self._write(0x87, [0xFF])
        self._write(0x88, [0x0A])
        self._write(0x89, [0x21])
        self._write(0x8A, [0x00])
        self._write(0x8B, [0x80])
        self._write(0x8C, [0x01])
        self._write(0x8D, [0x01])
        self._write(0x8E, [0xFF])
        self._write(0x8F, [0xFF])
        self._write(0xB6, [0x00,0x00])
        self._write(0x3A, [0x55])
        self._write(0x90, [0x08,0x08,0x08,0x08])
        self._write(0xBD, [0x06])
        self._write(0xBC, [0x00])
        self._write(0xFF, [0x60,0x01,0x04])
        self._write(0xC3, [0x13])
        self._write(0xC4, [0x13])
        self._write(0xC9, [0x22])
        self._write(0xBE, [0x11])
        self._write(0xE1, [0x10,0x0E])
        self._write(0xDF, [0x21,0x0c,0x02])
        self._write(0xF0, [0x45,0x09,0x08,0x08,0x26,0x2A])
        self._write(0xF1, [0x43,0x70,0x72,0x36,0x37,0x6F])
        self._write(0xF2, [0x45,0x09,0x08,0x08,0x26,0x2A])
        self._write(0xF3, [0x43,0x70,0x72,0x36,0x37,0x6F])
        self._write(0xED, [0x1B,0x0B])
        self._write(0xAE, [0x77])
        self._write(0xCD, [0x63])
        self._write(0x70, [0x07,0x07,0x04,0x0E,0x0F,0x09,0x07,0x08,0x03])
        self._write(0xE8, [0x34])

        self._write(0x62, [0x18,0x0D,0x71,0xED,0x70,0x70,0x18,0x0F,0x71,0xEF,0x70,0x70])
        self._write(0x63, [0x18,0x11,0x71,0xF1,0x70,0x70,0x18,0x13,0x71,0xF3,0x70,0x70])
        self._write(0x64, [0x28,0x29,0xF1,0x01,0xF1,0x00,0x07])
        self._write(0x66, [0x3C,0x00,0xCD,0x67,0x45,0x45,0x10,0x00,0x00,0x00])
        self._write(0x67, [0x00,0x3C,0x00,0x00,0x00,0x01,0x54,0x10,0x32,0x98])
        self._write(0x74, [0x10,0x85,0x80,0x00,0x00,0x4E,0x00])
        self._write(0x98, [0x3e,0x07])

        self._write(0x35)
        self._write(0x21)
        self._write(0x11)
        time.sleep(0.120)

        self._write(0x29)
        time.sleep(0.20)
  
    def SetWindows(self, Xstart, Ystart, Xend, Yend):
        #set the X coordinates
        self.command(0x2A)
        self.data(0x00)               #Set the horizontal starting point to the high octet
        self.data(Xstart)      #Set the horizontal starting point to the low octet
        self.data(0x00)               #Set the horizontal end to the high octet
        self.data(Xend - 1) #Set the horizontal end to the low octet 
        
        #set the Y coordinates
        self.command(0x2B)
        self.data(0x00)
        self.data(Ystart)
        self.data(0x00)
        self.data(Yend - 1)

        self.command(0x2C) 
    def FastImage(self, pix):
        self.spi_writebyte2(pix)		
        #l = len(pix)
        #for i in range(0,l,4096):
        #    self.spi_writebyte(pix[i:i+4096])		
    
    
    def ShowImage(self,Image):
        #print(">>> Writting to device %d" % self.dbgDevice)
        """Set buffer to value of Python Imaging Library image."""
        """Write display buffer to physical display"""
        imwidth, imheight = Image.size
        if imwidth != self.width or imheight != self.height:
            raise ValueError('Image must be same dimensions as display \
                ({0}x{1}).' .format(self.width, self.height))
        img = self.np.asarray(Image)
        pix = self.np.zeros((self.width,self.height,2), dtype = self.np.uint8)
        pix[...,[0]] = self.np.add(self.np.bitwise_and(img[...,[0]],0xF8),self.np.right_shift(img[...,[1]],5))
        pix[...,[1]] = self.np.add(self.np.bitwise_and(self.np.left_shift(img[...,[1]],3),0xE0),self.np.right_shift(img[...,[2]],3))
        pix = pix.flatten().tolist()
        self.SetWindows ( 0, 0, self.width, self.height)
        self.digital_write(self.DC_PIN, LCD_1inch28.global_GPIO.HIGH)
        for i in range(0,len(pix),4096):
            self.spi_writebyte(pix[i:i+4096])		
    
    def clear(self):
        """Clear contents of image buffer"""
        _buffer = [0xff]*(self.width * self.height * 2)
        self.SetWindows ( 0, 0, self.width, self.height)
        self.digital_write(self.DC_PIN, LCD_1inch28.global_GPIO.HIGH)
        for i in range(0,len(_buffer),4096):
            self.spi_writebyte(_buffer[i:i+4096])	        
        

