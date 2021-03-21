import xlsxwriter
from os import path
from Foundation import GenPTN
from Foundation import GenLabel_2

class TFT:
    "This function class is designed to generate coordinates for 3 terminals TFT used on silicon oxide wafer substrate."
    # All the units in this function class is [mm].

    def __init__(self,x=0,y=0,**kwargs):
        self.x = x
        self.y = y

        # variables in kwargs
        self.l = kwargs['l'] if 'l' in kwargs else 0.050          # channel length
        self.dl = kwargs['dl'] if 'dl' in kwargs else 0.010       # changing step of channel length
        self.w = kwargs['w'] if 'w' in kwargs else 2              # channel width
        self.dw = kwargs['dw'] if 'dw' in kwargs else 0           # changing step of channel width
        self.lg = kwargs['lg'] if 'lg' in kwargs else 1           # gate electrode length
        self.dlg = kwargs['dlg'] if 'dlg' in kwargs else 0        # changing step of gate electrode length
        self.w_semi = kwargs['semiconductor_width'] if 'semiconductor_width' in kwargs else 2.5  # Width of the semiconductor layer
        self.w_dielectric = kwargs['dielectric_width'] if 'dielectric_width' in kwargs else 4    # Width if the dielectric layer

        self.count = 10  # Number of devices for one set of device array
        self.dx = 2.5      # Distance between devices in x-axis
        self.dy = 0      # Distance between devices in y-axis
        self.shift_vec = [x + 3.5, y + 3.5]  # Vector for shifting calculated coordinates to the desired starting point
        self.translation_vec = [self.dx, self.dy]  # Vector for translating one device to a set of devices

        # The following part is written to determining the droplet spacing setting used to print each layer
        layer_list = ('contact', 'semiconductor', 'dielectric', 'gate', 'contact for gate')
        self.DropletSpacing = dict.fromkeys(layer_list, 20)
        if 'DropletSpacing' in kwargs:
            ds_in = kwargs['DropletSpacing']
            if isinstance(ds_in, dict):
                self.DropletSpacing.update(ds_in)
            elif isinstance(ds_in, list):
                for n in range(len(ds_in)):
                    self.DropletSpacing[layer_list[n]] = ds_in[n]
            elif isinstance(ds_in, int) or isinstance(ds_in, float):
                self.DropletSpacing = dict.fromkeys(layer_list, int(ds_in))

    def Contact(self):
        sv = self.shift_vec
        tv = self.translation_vec
        l0 = self.l
        dl = self.dl
        w0 = self.w
        dw = self.dw
        count = self.count

        square_list = []
        for n in range(count):
            w = w0+n*dw
            l = l0+n*dl
            x_shift = sv[0]+n*tv[0]
            y_shift = sv[1]+n*tv[1]
            square_list.append([-0.75+x_shift,-3.5+y_shift,1.5,1.5])
            square_list.append([-0.5+x_shift,-2+y_shift,1,1])
            square_list.append([-w/2.0+x_shift,-1+y_shift,w,1])
            square_list.append([-w/2.0+x_shift,l+y_shift,w,1])
            square_list.append([-0.5+x_shift,l+1+y_shift,1,1])
            square_list.append([-0.75+x_shift,l+2+y_shift,1.5,1.5])

        return square_list

    def Semiconductor(self):
        sv = self.shift_vec
        w_semi = self.w_semi
        l = self.dx
        count = self.count

        l_semi = 1+l*count
        square_list = []
        square_list.append([-1.5+sv[0],-w_semi/2.0+sv[1],l_semi,w_semi])

        return square_list

    def Dielectric(self):
        sv = self.shift_vec
        w_dielectric = self.w_dielectric
        l = self.dx
        count = self.count

        l_dielectric = 2+l*count
        square_list = []
        square_list.append([-2+sv[0],-w_dielectric/2.0+sv[1],l_dielectric,w_dielectric])

        return square_list

    def Gate(self):
        sv = self.shift_vec
        tv = self.translation_vec
        l0 = self.l
        dl = self.dl
        lg0 = self.lg
        dlg = self.dlg
        w = self.dx
        count = self.count

        square_list = []
        for n in range(count):
            l = l0+n*dl
            lg = lg0+n*dlg
            x_shift = sv[0]+n*tv[0]
            y_shift = sv[1]+n*tv[1]
            square_list.append([-w/2.0+x_shift,(l-lg)/2+y_shift,w,lg])

        #  加上两个扎针区的图案
        square_list.append([-3.5+sv[0],-2+sv[1],1.5,4])  # 左扎针区
        square_list.append([-2+sv[0],-0.5+sv[1],0.75,1])
        square_list.append([23.75+sv[0],-0.5+l/2.0+sv[1],1.25,1])  # 右扎针区
        square_list.append([25+sv[0],-2+sv[1],1.5,4])

        return square_list

    def Contact_for_gate(self):  # 单独生成栅极扎针区的图层，用于特种墨水打印的栅极，如：Graphene ink
        sv = self.shift_vec
        l0 = self.l
        dl = self.dl
        count = self.count
        l = l0+count*dl

        square_list = []
        square_list.append([-3.5+sv[0],-2+sv[1],1.5,4])  # 左扎针区
        square_list.append([25+sv[0],-2+sv[1],1.5,4])    # 右扎针区

        return square_list

    def Pattern(self,pattern):
        pattern_dict = {'contact':self.Contact(),
                        'semiconductor':self.Semiconductor(),
                        'dielectric':self.Dielectric(),
                        'gate':self.Gate(),
                        'contact for gate':self.Contact_for_gate()}
        return pattern_dict[pattern]

    def WritePattern(self,filename,saving_directory=path.dirname(__file__)):
        for n in ['contact']:
            pattern = self.Pattern(n)
            directory = saving_directory+filename+'_'+n+'.xlsx'

            file = xlsxwriter.Workbook(directory)
            pattern_sheet = file.add_worksheet()

            pattern_sheet.write(0, 0, 'X_Start')  # Writing title
            pattern_sheet.write(0, 1, 'Y_Start')
            pattern_sheet.write(0, 2, 'X_Width')
            pattern_sheet.write(0, 3, 'Y_Width')

            for i in range(len(pattern)):
                for j in range(len(pattern[0])):
                    pattern_sheet.write(i + 1, j, pattern[i][j])

            file.close()

        return

    def GeneratePatternSet(self, label, filename, saving_directory=path.dirname(__file__)):
        ptn = GenPTN.ptn()
        genlabel = GenLabel_2.Label(markersize=3,fontsize=2,character_distance=0.2)

        for n in ['contact', 'semiconductor', 'dielectric', 'gate', 'contact for gate']:
            if n == 'contact for gate':
                marking = genlabel.Marker('3', 0, 0)
            else:
                marking = genlabel.Marker(n, 0, 0)
            if n == 'contact':
                text = genlabel.Text(label, 3.5, 0)
            else:
                text = []
            pattern = marking + text + self.Pattern(n)

            directory = saving_directory + filename + '_' + n + '.xlsx'

            file = xlsxwriter.Workbook(directory)
            pattern_sheet = file.add_worksheet()

            pattern_sheet.write(0, 0, 'X_Start')  # Writing title
            pattern_sheet.write(0, 1, 'Y_Start')
            pattern_sheet.write(0, 2, 'X_Width')
            pattern_sheet.write(0, 3, 'Y_Width')

            for i in range(len(pattern)):
                for j in range(len(pattern[0])):
                    pattern_sheet.write(i + 1, j, pattern[i][j])

            file.close()

            ptn.PreviewPattern(directory, filename + '_' + n, saving_directory,X_unitcell=6000,Y_unitcell=3000,scale=200)
            ptn.ExcelToPTN(directory, filename + '_' + n, saving_directory, X_total=40.025, Y_total=15.025,DropletSpacing=self.DropletSpacing[n], X_unitcell=35, Y_unitcell=15)

        return


