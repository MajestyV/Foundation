import array

class bmp:
    """ bmp data structure """

    # Using micrometer (um) as unit
    def __init__(self, w=1920, h=1080, unitcell_w=100, unitcell_h=100, mode='Top-Down'):
        self.w = w
        self.h = h
        self.w0 = unitcell_w
        self.h0 = unitcell_h
        self.mode = mode


    def calc_data_size (self):
        if((self.w*3)%4 == 0):
            self.dataSize = self.w * 3 * self.h
        else:
            self.dataSize = (((self.w * 3) // 4 + 1) * 4) * self.h

        self.fileSize = self.dataSize + 54

    def conv2byte(self, l, num, len):
        tmp = num
        for i in range(len):
            l.append(tmp & 0x000000ff)
            tmp >>= 8

    def gen_bmp_header (self):
        self.calc_data_size()
        self.bmp_header = [0x42, 0x4d]
        self.conv2byte(self.bmp_header, self.fileSize, 4)                   #file size
        self.conv2byte(self.bmp_header, 0, 2)
        self.conv2byte(self.bmp_header, 0, 2)
        self.conv2byte(self.bmp_header, 54, 4)                              #rgb data offset
        self.conv2byte(self.bmp_header, 40, 4)                              #info block size
        self.conv2byte(self.bmp_header, self.w, 4)
        if self.mode == 'Top-Down':                                         # If the height of BMP file in the header is negative, the bmp picture will be scanned in a top-down sequence
            self.conv2byte(self.bmp_header, -self.h, 4)
        elif self.mode == 'Bottom-Up':
            self.conv2byte(self.bmp_header, self.h, 4)
        self.conv2byte(self.bmp_header, 1, 2)
        self.conv2byte(self.bmp_header, 24, 2)                              #888
        self.conv2byte(self.bmp_header, 0, 4)                               #no compression
        self.conv2byte(self.bmp_header, self.dataSize, 4)                   #rgb data size
        self.conv2byte(self.bmp_header, 0, 4)
        self.conv2byte(self.bmp_header, 0, 4)
        self.conv2byte(self.bmp_header, 0, 4)
        self.conv2byte(self.bmp_header, 0, 4)

    def print_bmp_header (self):
        length = len(self.bmp_header)
        for i in range(length):
            print("{:0>2x}".format(self.bmp_header[i]), end=' ')
            if i%16 == 15:
                print('')
        print('')

    def paint_bgcolor(self, color=0xffffff):
        self.rgbData = []
        for r in range(self.h):
            self.rgbDataRow = []
            for c in range(self.w):
                self.rgbDataRow.append(color)
            self.rgbData.append(self.rgbDataRow)

    def paint_line(self, x1, y1, x2, y2, color=0x000000):
        if x1 == x2:
            x = x1
            for y in range(y1,y2+1):
                self.rgbData[y][x] = color
        elif y1 == y2:
            y = y1
            for x in range(x1,x2+1):
                self.rgbData[y][x] = color
        else:
            k = (y2 - y1) / (x2 - x1)
            for x in range(x1, x2 + 1):
                y = int(k * (x - x1) + y1)
                self.rgbData[y][x] = color

    def paint_rect(self, x1, y1, w, h, color=0x000000):
        for x in range(x1, x1 + w):
            for y in range(y1, y1 + h):
                self.rgbData[y][x] = color

    def paint_unitcell(self,x1,y1,w,h,x_count=1,y_count=1,color=0x000000,ShowSeperationLine=1):
        if ShowSeperationLine == 1:
            for i in range(x_count): self.paint_line(i*self.w0,0,i*self.w0,self.h-1)
            for j in range(y_count): self.paint_line(0,j*self.h0,self.w-1,j*self.h0)

        for i in range(x_count):
            for j in range(y_count):
                self.paint_rect(x1+i*self.w0,y1+j*self.h0,w,h,color)

    def save_image(self, name="save.bmp"):
        f = open(name, 'wb')

        # write bmp header
        f.write(array.array('B', self.bmp_header).tobytes())

        # write rgb data
        zeroBytes = self.dataSize // self.h - self.w * 3

        for r in range(self.h):
            l = []
            for i in range(len(self.rgbData[r])):
                p = self.rgbData[r][i]
                l.append(p & 0x0000ff)
                p >>= 8
                l.append(p & 0x0000ff)
                p >>= 8
                l.append(p & 0x0000ff)

            f.write(array.array('B', l).tobytes())

            for i in range(zeroBytes):
                f.write(bytes([0x00]))

        # close file
        f.close()

if __name__ == '__main__':
    image = bmp(500, 500,100,100)
    image.gen_bmp_header()
    image.print_bmp_header()

    image.paint_bgcolor() # This line must be executed to create the rgbData object

    #image.paint_line(50, 50, 450, 450, 0xff0000)
    #image.paint_rect(100, 100, 100, 200)

    image.paint_unitcell(0,0,50,50,5,5)

    desktop_directory = 'C:/Users/Majes/Desktop/Testing/'

    image.save_image(desktop_directory+"save1.bmp")