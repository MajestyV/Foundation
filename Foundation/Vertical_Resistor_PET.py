import xlsxwriter
from os import path
from Foundation import GenPTN
from Foundation import GenLabel_2

class Resistor:
    "This function class is designed to generate coordinates for resistor or similar device like photodetector (photoresistor type)."
    # All the units in this function class is [mm].

    def __init__(self,x=0,y=0,**kwargs):
        self.x = x
        self.y = y

        # variables in kwargs
        self.w_top = kwargs['w_top'] if 'w_top' in kwargs else 0.500      # width of top electrode
        self.dw_top = kwargs['dw_top'] if 'dw_top' in kwargs else 0.100   # changing step of top electrode width
        self.w_bottom = kwargs['w_bottom'] if 'w_bottom' in kwargs else 0.500       # width of bottom electrode
        self.dw_bottom = kwargs['dw_bottom'] if 'dw_bottom' in kwargs else 0.100    # changing step of bottom electrode width
        # effective sensing area = w_top*w_bottom
        #self.lg = kwargs['lg'] if 'lg' in kwargs else 1  # gate electrode length
        #self.dlg = kwargs['dlg'] if 'dlg' in kwargs else 0  # changing step of gate electrode length
        self.w_resistive = kwargs['resistive_width'] if 'resistive_width' in kwargs else 2.5  # width of the resistive layer
        #self.w_dielectric = kwargs['dielectric_width'] if 'dielectric_width' in kwargs else 4  # Width if the dielectric layer

        self.count = kwargs['num_device'] if 'num_device' in kwargs else 10 # Number of devices for one set of device array
        self.dx = kwargs['x_distance'] if 'x_distance' in kwargs else 8 # Distance between devices in x-axis
        self.dy = kwargs['y_distance'] if 'y_distance' in kwargs else 0 # Distance between devices in y-axis
        self.shift_vec = [x + 3.5, y + 3.5]  # Vector for shifting calculated coordinates to the desired starting point
        self.translation_vec = [self.dx, self.dy]  # Vector for translating one device to a set of devices

        # The following part is written to determining the droplet spacing setting used to print each layer
        layer_list = ('bottom', 'resistive', 'top', 'contact for bottom', 'contact for top', 'contact for both')
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

    def Bottom(self):
        sv = self.shift_vec
        tv = self.translation_vec
        w0 = self.w_bottom
        dw = self.dw_bottom
        count = self.count

        square_list = []
        for n in range(count):
            w = w0 + n * dw
            x_shift = sv[0] + n * tv[0]
            y_shift = sv[1] + n * tv[1]
            square_list.append([-0.75 + x_shift, 3.5 + y_shift, 1.5, 1.5])
            square_list.append([-w/2.0 + x_shift, 2 + y_shift, w, 4])
            square_list.append([-0.75 + x_shift, -2 + y_shift, 1.5, 1.5])

        return square_list

    def Resistive(self):
        sv = self.shift_vec
        tv = self.translation_vec
        w = self.w_resistive
        count = self.count

        square_list = []
        for n in range(count):
            x_shift = sv[0]+n*tv[0]
            y_shift = sv[1]+n*tv[1]
            square_list.append([-w/2.0 + x_shift, -w/2.0 + y_shift, w, w])

        return square_list

    def Top(self):
        sv = self.shift_vec
        tv = self.translation_vec
        w0 = self.w_top
        dw = self.dw_top
        count = self.count

        square_list = []
        for n in range(count):
            w = w0 + n * dw
            x_shift = sv[0] + n * tv[0]
            y_shift = sv[1] + n * tv[1]
            square_list.append([-3.5 + x_shift, 0.75 + y_shift, 1.5, 1.5])
            square_list.append([-2 + x_shift, w/2.0 + y_shift, 4, w])
            square_list.append([2 + x_shift, 0.75 + y_shift, 1.5, 1.5])

        return square_list

    # 这个函数可用于生成用于连接顶电极或者底电极的扎针区的信息
    def Contact_for_bottom(self):
        sv = self.shift_vec
        tv = self.translation_vec
        count = self.count

        square_list = []
        for n in range(count):
            x_shift = sv[0]+n*tv[0]
            y_shift = sv[1]+n*tv[1]
            square_list.append([-1+x_shift,3.5+y_shift,2,1.5])
            square_list.append([-1+x_shift,-2+y_shift,2,1.5])

        return square_list

    def Contact_for_top(self):
        sv = self.shift_vec
        tv = self.translation_vec
        count = self.count

        square_list = []
        for n in range(count):
            x_shift = sv[0] + n * tv[0]
            y_shift = sv[1] + n * tv[1]
            square_list.append([-3.5 + x_shift, 1 + y_shift, 1.5, 2])
            square_list.append([2 + x_shift, 1 + y_shift, 1.5, 2])

        return square_list

    def Contact_for_both(self):
        contact_for_bottom = self.Contact_for_bottom()
        contact_for_top = self.Contact_for_top()
        square_list = contact_for_bottom+contact_for_top
        return square_list

    def Pattern(self, pattern):
        pattern_dict = {'bottom': self.Bottom(),
                        'resistive': self.Resistive(),
                        'top': self.Top(),
                        'contact for bottom': self.Contact_for_bottom(),
                        'contact for top': self.Contact_for_top(),
                        'contact for both': self.Contact_for_both()}
        return pattern_dict[pattern]

    #def WritePattern(self, filename, saving_directory=path.dirname(__file__)):
        #for n in ['bottom']:
            #pattern = self.Pattern(n)
            #directory = saving_directory + filename + '_' + n + '.xlsx'

            #file = xlsxwriter.Workbook(directory)
            #pattern_sheet = file.add_worksheet()

            #pattern_sheet.write(0, 0, 'X_Start')  # Writing title
            #pattern_sheet.write(0, 1, 'Y_Start')
            #pattern_sheet.write(0, 2, 'X_Width')
            #pattern_sheet.write(0, 3, 'Y_Width')

            #for i in range(len(pattern)):
                #for j in range(len(pattern[0])):
                    #pattern_sheet.write(i + 1, j, pattern[i][j])

            #file.close()

        #return

    def GeneratePatternSet(self, label, filename, saving_directory=path.dirname(__file__)):
        ptn = GenPTN.ptn()
        genlabel = GenLabel_2.Label(markersize=3, fontsize=2, character_distance=0.2)

        for n in ['bottom', 'resistive', 'top', 'contact for bottom', 'contact for top', 'contact for both']:
            # Selecting alignment marker
            if n == 'bottom':
                marker = genlabel.Marker('0', 0, 0)  # 调用genlabel.Marker函数时，即使用序号来调用都要以字符串形式输入对准标记的序号
            elif n == 'resistive':
                marker = genlabel.Marker('1', 0, 0)
            elif n =='top':
                marker = genlabel.Marker('2', 0, 0)
            else:
                marker = genlabel.Marker('3', 0, 0)
            # Generating text label
            if n == 'bottom':
                text = genlabel.Text(label, 3.5, 0)
            else:
                text = []
            pattern = marker + text + self.Pattern(n)

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

            ptn.PreviewPattern(directory, filename + '_' + n, saving_directory, X_unitcell=8000, Y_unitcell=1800, scale=100)
            ptn.ExcelToPTN(directory, filename + '_' + n, saving_directory, X_total=100.025, Y_total=20.025, DropletSpacing=self.DropletSpacing[n], X_unitcell=100, Y_unitcell=20)

        return