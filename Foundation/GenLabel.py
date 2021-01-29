import xlsxwriter
from os import path
from Foundation import GenPTN

class Label:
    """ This script is designed to generate text label patterns."""

    def __init__(self,x=0,y=0,fontsize=2.5,linewidth=0.2,distance=0.4):
        self.x = x
        self.y = y
        self.w = fontsize
        self.l = linewidth
        self.d = distance

    def MarkingLabel_0(self,x=0, y=0, width=5, linewidth=0.05, origin_size=0.05):
        square = []
        square.append([x, y, origin_size, origin_size])  # origin
        square.append([x, y + 0.4 * width, 0.4 * width, linewidth])
        square.append([x, y + 0.6 * width, 0.4 * width, linewidth])
        square.append([x + 0.6 * width, y + 0.4 * width, 0.4 * width, linewidth])
        square.append([x + 0.6 * width, y + 0.6 * width, 0.4 * width, linewidth])
        square.append([x + 0.4 * width, y, linewidth, 0.4 * width])
        square.append([x + 0.6 * width, y, linewidth, 0.4 * width])
        square.append([x + 0.4 * width, y + 0.6 * width, linewidth, 0.4 * width])
        square.append([x + 0.6 * width, y + 0.6 * width, linewidth, 0.4 * width])
        return square

    def MarkingLabel_1(self,x=0, y=0, width=5, linewidth=0.5, origin_size=0.05):
        square = []
        square.append([x, y, origin_size, origin_size])  # origin
        square.append([x, y + (width - linewidth) / 2.0, width, linewidth])
        square.append([x + (width - linewidth) / 2.0, y, linewidth, width])
        return square

    def MarkingLabel_2(self,x=0, y=0, width=5, square_size=1, origin_size=0.05):
        square = []
        square.append([x, y, origin_size, origin_size])  # origin
        square.append([x + 0.1 * width, y + 0.1 * width, square_size, square_size])
        square.append([x + 0.1 * width, y + 0.7 * width, square_size, square_size])
        square.append([x + 0.7 * width, y + 0.1 * width, square_size, square_size])
        square.append([x + 0.7 * width, y + 0.7 * width, square_size, square_size])
        return square

    def MarkingLabel_3(self,x=0, y=0, width=5, linewidth=0.05, origin_size=0.05):
        square = []
        square.append([x, y, origin_size, origin_size])  # origin
        square.append([x, y, width, linewidth])
        square.append([x, y, linewidth, width])
        square.append([x + width, y, linewidth, width])
        square.append([x, y + width, width, linewidth])
        return square

    def Letter_B(self,x,y):
        w = self.w
        l = self.l
        text = []
        text.append([x,y,l,2*w])
        text.append([x,y,6*l,l])
        text.append([x+6*l,y+l,2*l,l])
        text.append([x+8*l,y+2*l,2*l,l])
        text.append([x+9*l,y+3*l,2*l,l])
        text.append([x+11*l,y+4*l,l,5*l])
        text.append([x+9*l,y+9*l,2*l,l])
        text.append([x+8*l,y+10*l,2*l,l])
        text.append([x+6*l,y+11*l,2*l,l])
        text.append([x,y+12*l,6*l,l])
        text.append([x+6*l,y+13*l,2*l,l])
        text.append([x+8*l,y+14*l,2*l,l])
        text.append([x+9*l,y+15*l,2*l,l])
        text.append([x+11*l,y+16*l,l,5*l])
        text.append([x+9*l,y+21*l,2*l,l])
        text.append([x+8*l,y+22*l,2*l,l])
        text.append([x+6*l,y+23*l,2*l,l])
        text.append([x,y+24*l,6*l,l])
        return text

    def Letter_G(self,x,y):
        w = self.w
        l = self.l
        text =[]
        text.append([x+5*l,y,3*l,l])       # line 0
        text.append([x+4*l,y+l,l,l])       # line 1
        text.append([x+8*l,y+l,2*l,l])
        text.append([x+3*l,y+2*l,l,l])     # line 2
        text.append([x+9*l,y+2*l,2*l,l])
        text.append([x+2*l,y+3*l,l,l])     # line 3
        text.append([x+10*l,y+3*l,l,l])
        text.append([x+l,y+4*l,l,3*l])     # line 4
        text.append([x+11*l,y+4*l,l,3*l])
        text.append([x,y+7*l,l,13*l])      # line 7
        text.append([x+7*l,y+15*l,5*l,l])  # line 15
        text.append([x+11*l,y+16*l,l,5*l]) # line 16
        text.append([x+l,y+20*l,l,2*l])    # line 20
        text.append([x+10*l,y+20*l,l,4*l])
        text.append([x+2*l,y+22*l,l,l])    # line 22
        text.append([x+3*l,y+23*l,l,l])    # line 23
        text.append([x+9*l,y+23*l,2*l,l])
        text.append([x+4*l,y+24*l,6*l,l])  # line 24
        return text

    def Letter_L(self,x,y):
        w = self.w
        l = self.l
        text = []
        text.append([x,y,l,2*w])
        text.append([x,y+2*w-l,w,l])
        return text

    def Letter_T(self,x,y):
        w = self.w
        l = self.l
        text = []
        text.append([x,y,w,2*l])
        text.append([x+(w-l)/2.0,y,l,2*w])
        return text

    def zero(self,x,y):
        w = self.w
        l = self.l
        text = []
        text.append([x,y,w,l])
        text.append([x+w-l,y,l,2*w])
        text.append([x,y+2*w-l,w,l])
        text.append([x,y,l,2*w])
        return text

    def one(self,x,y):
        w = self.w
        l = self.l
        text = []
        text.append([x+w-l,y,l,2*w])
        return text

    def two(self,x,y):
        w = self.w
        l = self.l
        text = []
        text.append([x,y,w,l])
        text.append([x+w-l,y,l,w])
        text.append([x,y+w-l/2.0,w,l])
        text.append([x,y+w,l,w])
        text.append([x,y+2*w-l,w,l])
        return text

    def three(self,x,y):
        w = self.w
        l = self.l
        text = []
        text.append([x,y,w,l])
        text.append([x+w-l,y,l,2*w])
        text.append([x,y+w-l/2.0,w,l])
        text.append([x,y+2*w-l,w,l])
        return text

    def four(self,x,y):
        w = self.w
        l = self.l
        text = []
        text.append([x,y,l,w])
        text.append([x,y+w-l/2.0,w,l])
        text.append([x+w-l,y,l,2*w])
        return text

    def five(self,x,y):
        w = self.w
        l = self.l
        text = []
        text.append([x,y,w,l])
        text.append([x,y,l,w])
        text.append([x,y+w-l/2.0,w,l])
        text.append([x+w-l,y+w,l,w])
        text.append([x,y+2*w-l,w,l])
        return text

    def six(self,x,y):
        w = self.w
        l = self.l
        text = []
        text.append([x,y,w,l])
        text.append([x,y,l,2*w])
        text.append([x,y+2*w-l,w,l])
        text.append([x+w-l,y+w,l,w])
        text.append([x,y+w-l/2.0,w,l])
        return text

    def seven(self,x,y):
        w = self.w
        l = self.l
        text = []
        text.append([x,y,w,l])
        text.append([x+w-l,y,l,2*w])
        return text

    def eight(self,x,y):
        w = self.w
        l = self.l
        text = []
        text.append([x,y,w,l])
        text.append([x,y,l,2*w])
        text.append([x+w-l,y,l,2*w])
        text.append([x,y+w-l/2.0,w,l])
        text.append([x,y+2*w-l,w,l])
        return text

    def nine(self,x,y):
        w = self.w
        l = self.l
        text = []
        text.append([x,y,w,l])
        text.append([x,y,l,w])
        text.append([x,y+w-l/2.0,w,l])
        text.append([x+w-l,y,l,2*w])
        text.append([x,y+2*w-l,w,l])
        return text

    def dash(self,x,y):
        w = self.w
        l = self.l
        text = []
        text.append([x,y+w-l/2.0,w,l])
        return text

    def Reference(self,character,x,y):
        reference_dict = {'B':self.Letter_B(x,y),
                          'G':self.Letter_G(x,y),
                          'L':self.Letter_L(x,y),
                          'T':self.Letter_T(x,y),
                          '0':self.zero(x,y),
                          '1':self.one(x,y),
                          '2':self.two(x,y),
                          '3':self.three(x,y),
                          '4':self.four(x,y),
                          '5':self.five(x,y),
                          '6':self.six(x,y),
                          '7':self.seven(x,y),
                          '8':self.eight(x,y),
                          '9':self.nine(x,y),
                          '-':self.dash(x,y)}
        return reference_dict[character]

    # Pattern writing modules
    def Pattern(self):  # This function is written to test the shape of patterns
        self.pattern_data = []

    def MakeMarking(self,mode,x=0,y=0,w=5):
        dict = {'0':self.MarkingLabel_0(x,y,w),
                '1':self.MarkingLabel_1(x,y,w),
                '2':self.MarkingLabel_2(x,y,w),
                '3':self.MarkingLabel_3(x,y,w),
                'contact':self.MarkingLabel_0(x,y,w),
                'semiconductor':self.MarkingLabel_1(x,y,w),
                'dielectric':self.MarkingLabel_2(x,y,w),
                'gate':self.MarkingLabel_3(x,y,w),
                'gate_dualports':self.MarkingLabel_3(x,y,w)}
        #self.pattern_data = self.pattern_data+dict[mode]
        return dict[mode]

    def Text(self,text,x=0,y=0,distance=""):
        if not distance:
            distance = self.d
        text_pattern = []
        i = 0
        for character in text:
            text_pattern = text_pattern+self.Reference(character,x+i*(distance+self.w),y)
            i = i+1

        #self.pattern_data = self.pattern_data+text_pattern
        return text_pattern

    def Pattern_write(self,file_name,saving_directory=path.dirname(__file__)):
        file_path = saving_directory+file_name+'.xlsx'

        file = xlsxwriter.Workbook(file_path)
        pattern_sheet = file.add_worksheet()

        pattern_sheet.write(0,0,'X_Start')  # Writing title
        pattern_sheet.write(0,1,'Y_Start')
        pattern_sheet.write(0,2,'X_Width')
        pattern_sheet.write(0,3,'Y_Width')

        for i in range(len(self.pattern_data)):
            for j in range(len(self.pattern_data[0])):
                pattern_sheet.write(i+1,j,self.pattern_data[i][j])

        file.close()


if __name__ == '__main__':
    gl = Label()
    gp = GenPTN.ptn()
    filename = '3T_label_3'
    saving_directory = "C:/Users/Majes/Desktop/Testing/HelloWorld2/3T/"

    #result = gl.Text('0123456789-',0,0,filename,saving_directory)
    #print(result)

    gl.Pattern()
    gl.MakeMarking('3',0,0,5)
    #gl.Text('3TTG-2020-11-18',6,0)
    gl.Pattern_write(filename,saving_directory)

    gp.PreviewPattern(saving_directory+filename+'.xlsx',filename,saving_directory,2000,400,40)