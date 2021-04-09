import xlsxwriter
from os import path
from Foundation import GenPTN
from Foundation import GenLabel_2

class TFT:
    "This function class is designed to generate coordinates for 3 terminals TFT used on silicon oxide wafer substrate."
    # All the units in this function class is [mm].

    def __init__(self,x=0,y=5,**kwargs):
        self.x = x  # Starting point of the pattern
        self.y = y
        self.x_label = kwargs['x_label'] if 'x_label' in kwargs else 0  # Starting point of the label pattern
        self.y_label = kwargs['y_label'] if 'y_label' in kwargs else 0

        # variables in kwargs
        self.l = kwargs['l'] if 'l' in kwargs else 0.050          # channel length
        self.dl = kwargs['dl'] if 'dl' in kwargs else 0.010       # changing step of channel length
        self.w = kwargs['w'] if 'w' in kwargs else 1              # channel width
        self.dw = kwargs['dw'] if 'dw' in kwargs else 0           # changing step of channel width
        self.lg = kwargs['lg'] if 'lg' in kwargs else 1           # gate electrode length
        self.dlg = kwargs['dlg'] if 'dlg' in kwargs else 0        # changing step of gate electrode length
        self.w_semi = kwargs['semiconductor_width'] if 'semiconductor_width' in kwargs else 2  # Width of the semiconductor layer
        self.w_dielectric = kwargs['dielectric_width'] if 'dielectric_width' in kwargs else 4    # Width if the dielectric layer

        self.num_device = 10
        self.translation_vec = [2.5, 0]  # Vector for translating one device to a set of devices

        # 这个标签可以将整个器件的版图沿 y=x 翻转
        self.coordinate = kwargs['coordinate'] if 'coordinate' in kwargs else 'normal'
        # 定义unitcell的大小
        self.X_unitcell = kwargs['X_unitcell'] if 'X_unitcell' in kwargs else 35
        self.Y_unitcell = kwargs['Y_unitcell'] if 'Y_unitcell' in kwargs else 15
        # 定义用于preview pattern的BMP图中器件的放大倍数
        self.scale = kwargs['preview_scale'] if 'preview_scale' in kwargs else 200

        # The following part is written to determining the droplet spacing setting used to print each layer
        layer_list = ('contact', 'semiconductor', 'dielectric', 'gate', 'contact for contact', 'contact for gate', 'contact for all')
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
        tv = self.translation_vec
        l0 = self.l
        dl = self.dl
        w0 = self.w
        dw = self.dw
        num_device = self.num_device

        square_list = []
        for n in range(num_device):
            w = w0+n*dw
            l = l0+n*dl
            x_shift = self.x+n*tv[0]
            y_shift = self.y+n*tv[1]
            square_list.append([2.5+x_shift,y_shift,1.5,1.5])
            square_list.append([2.75+x_shift,1.5+y_shift,1,1])
            square_list.append([3.25-w/2.0+x_shift,2.5+y_shift,w,1])
            square_list.append([3.25-w/2.0+x_shift,3.5+l+y_shift,w,1-l])
            square_list.append([2.75+x_shift,4.5+y_shift,1,1])
            square_list.append([2.5+x_shift,5.5+y_shift,1.5,1.5])

        return square_list

    def Semiconductor(self):
        w_semi = self.w_semi

        square_list = [[2+self.x,3.5-w_semi/2.0+self.y,25,w_semi]]

        return square_list

    def Dielectric(self):
        w_dielec = self.w_dielectric

        square_list = [[1.5 + self.x, 3.5 - w_dielec / 2.0 + self.y, 26, w_dielec]]

        return square_list

    def Gate(self):
        tv = self.translation_vec
        l0 = self.l
        dl = self.dl
        lg0 = self.lg
        dlg = self.dlg
        num_device = self.num_device

        square_list = []
        for n in range(num_device):
            l = l0+n*dl
            lg = lg0+n*dlg
            x_shift = self.x+n*tv[0]
            y_shift = self.y+n*tv[1]
            square_list.append([2+x_shift,3.5+(l-lg)/2.0+y_shift,2.5,lg])

        #  加上两个扎针区的图案
        square_list.append([self.x, 1.5 + self.y, 1.5, 4])  # 左扎针区
        square_list.append([1.5 + self.x, 3 + self.y, 0.5, 1])
        square_list.append([27 + self.x, 3 + self.y, 0.5, 1])  # 右扎针区
        square_list.append([27.5 + self.x, 1.5 + self.y, 1.5, 4])

        return square_list

    def Contact_for_contact(self):  # 单独生成源漏极扎针区的图层，用于特种墨水打印的栅极，如：Graphene ink
        tv = self.translation_vec
        num_device = self.num_device

        square_list = []
        for n in range(num_device):
            x_shift = self.x + n * tv[0]
            y_shift = self.y + n * tv[1]
            square_list.append([2.5 + x_shift, y_shift, 1.5, 1.5])
            square_list.append([2.5 + x_shift, 5.5 + y_shift, 1.5, 1.5])

        return square_list

    def Contact_for_gate(self):  # 单独生成栅极扎针区的图层，用于特种墨水打印的栅极，如：Graphene ink
        square_list = []
        square_list.append([self.x, 1.5 + self.y, 1.5, 4])  # 左扎针区
        square_list.append([27.5 + self.x, 1.5 + self.y, 1.5, 4])  # 右扎针区

        return square_list

    def Contact_for_all(self):
        square_list = self.Contact_for_contact() + self.Contact_for_gate()
        return square_list

    def Pattern(self,pattern):
        pattern_dict = {'contact':self.Contact(),
                        'semiconductor':self.Semiconductor(),
                        'dielectric':self.Dielectric(),
                        'gate':self.Gate(),
                        'contact for contact': self.Contact_for_contact(),
                        'contact for gate': self.Contact_for_gate(),
                        'contact for all': self.Contact_for_all()}
        return pattern_dict[pattern]

    # 用于将版图X，Y坐标翻转的模块
    def FlipPattern(self, pattern):
        for n in range(len(pattern)):
            x, y, x_width, y_width = pattern[n]
            pattern[n] = [y, x, y_width, x_width]
        return pattern

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
        X_unitcell = self.X_unitcell
        Y_unitcell = self.Y_unitcell

        for n in ['contact', 'semiconductor', 'dielectric', 'gate', 'contact for contact', 'contact for gate', 'contact for all']:
            if (n in ['contact for contact', 'contact for gate', 'contact for all']):
                marking = genlabel.Marker('3', self.x_label, self.y_label)
            else:
                marking = genlabel.Marker(n, self.x_label, self.y_label)
            if n == 'contact':
                text = genlabel.Text(label, self.x_label+3.5, self.y_label)
            else:
                text = []
            pattern = marking + text + self.Pattern(n)

            if self.coordinate == 'flip':
                pattern = self.FlipPattern(pattern)
                X_unitcell = self.Y_unitcell  # 这里不能用Y_unitcell，不然每次循环都会把unitcell的长跟宽调换，要用不受影响的全局变量
                Y_unitcell = self.X_unitcell

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

            ptn.PreviewPattern(directory, filename + '_' + n, saving_directory,X_unitcell=X_unitcell*self.scale,Y_unitcell=Y_unitcell*self.scale,scale=self.scale)
            ptn.ExcelToPTN(directory, filename + '_' + n, saving_directory, X_total=X_unitcell+0.025, Y_total=Y_unitcell+0.025,DropletSpacing=self.DropletSpacing[n], X_unitcell=X_unitcell, Y_unitcell=Y_unitcell)

        return