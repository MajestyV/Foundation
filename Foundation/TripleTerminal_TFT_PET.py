import xlsxwriter
from os import path
from Foundation import GenPTN
from Foundation import GenLabel

class TFT:
    "This function class is designed to generate coordinates for 3 terminals TFT set used on PET substrate."
    # All the units in this function class is [mm].

    def __init__(self,x=0,y=0,**kwargs):
        self.x = x   # Setting the origin (x,y) for the pattern
        self.y = y

        # variables in kwargs
        self.l = kwargs['l'] if 'l' in kwargs else 0.050                            # l is the channel length of the first TFT in the set
        self.dl = kwargs['dl'] if 'dl' in kwargs else 0.010                         # dl is the changing step of channel length, the nth device will have a channel length of l0+(n-1)*dl
        self.w = kwargs['w'] if 'w' in kwargs else 2                                # w is the channel width of the first TFT in the set
        self.dw = kwargs['dw'] if 'dw' in kwargs else 0                             # In general, the channel width of the whole set of devices are the same, in other words, dw = 0
        self.lg = kwargs['lg'] if 'lg' in kwargs else 1                             # lg the is length of the gate electrode, and the default value is 1 mm
        self.dlg = kwargs['dlg'] if 'dlg' in kwargs else 0                          # Changing step of lg, set to 0 as default value (lg remains constant)
        self.count = kwargs['num_device'] if 'num_device' in kwargs else 10         # Number of devices in one pattern set, default =10
        self.dx = kwargs['x_distance'] if 'x_distance' in kwargs else 8             # Distance between devices in x-axis, default = 8mm
        self.dy = kwargs['y_distance'] if 'y_distance' in kwargs else 0             # Distance between devices in y-axis, default = 0
        self.w_semi = kwargs['semiconductor_width'] if 'semiconductor_width' in kwargs else 4  # Width of the semiconductor and dielectric layer
        # self.device_size = kwargs['device_size'] if 'device_size' in kwargs else 8  # The length of one size of the device, regarding the device is square as default

        self.shift_vec = [x+3.5,y+3.5]             # Vector for shifting calculated coordinates to the desired starting point
        self.translation_vec = [self.dx,self.dy]   # Vector for translating one device to a set of devices


        # The following part is written to determining the droplet spacing setting used to print each layer
        layer_list = ('contact','semiconductor','dielectric','gate','gate_dualports')
        self.DropletSpacing = dict.fromkeys(layer_list,20)
        if 'DropletSpacing' in kwargs:
            ds_in = kwargs['DropletSpacing']
            if isinstance(ds_in,dict):
                self.DropletSpacing.update(ds_in)
            elif isinstance(ds_in,list):
                for n in range(len(ds_in)):
                    self.DropletSpacing[layer_list[n]] = ds_in[n]
            elif isinstance(ds_in,int) or isinstance(ds_in,float):
                self.DropletSpacing = dict.fromkeys(layer_list,int(ds_in))

    def Contact(self):
        sv = self.shift_vec         # Shifting vector
        tv = self.translation_vec   # Translation vector
        l0 = self.l
        dl = self.dl
        w0 = self.w
        dw = self.dw
        count = self.count

        square_list = []
        for n in range(count):
            w = w0+n*dw
            l = l0+n*dl
            x_shift = sv[0]+n*tv[0]   # Actual shifting amount in x-axis for nth device
            y_shift = sv[1]+n*tv[1]   # Actual shifting amount in y-axis for nth device
            square_list.append([-1+x_shift,-3.5+y_shift,2,1.5])
            square_list.append([-0.5+x_shift,-2+y_shift,1,1])
            square_list.append([-w/2.0+x_shift,-1+y_shift,w,1])
            square_list.append([-w/2.0+x_shift,l+y_shift,w,1])
            square_list.append([-0.5+x_shift,l+1+y_shift,1,1])
            square_list.append([-1+x_shift,l+2+y_shift,2,1.5])

        #contact_electrode = []
        #for n in range(len(square_list)):
            #contact_electrode = contact_electrode+square_list[n]

        return square_list

    def Semiconductor(self):
        sv = self.shift_vec
        tv = self.translation_vec
        w_semi = self.w_semi
        count = self.count

        square_list = []
        for n in range(count):
            x_shift = sv[0]+n*tv[0]
            y_shift = sv[1]+n*tv[1]
            square_list.append([-w_semi/2.0+x_shift,-w_semi/2.0+y_shift,w_semi,w_semi])

        return square_list

    def Gate(self):
        sv = self.shift_vec
        tv = self.translation_vec
        l0 = self.l
        dl = self.dl
        w0 = self.w
        dw = self.dw
        lg0 = self.lg
        dlg = self.dlg
        count = self.count

        square_list = []
        for n in range(count):
            l = l0+n*dl
            w = w0+n*dw
            lg = lg0+n*dlg
            x_shift = sv[0]+n*tv[0]
            y_shift = sv[1]+n*tv[1]
            square_list.append([-w/2.0+x_shift,(l-lg)/2.0+y_shift,2+w/2.0,lg])
            square_list.append([2+x_shift,-1+y_shift,1.5,2])

        return square_list

    def Gate_DualContact(self):
        sv = self.shift_vec
        tv = self.translation_vec
        l0 = self.l
        dl = self.dl
        lg0 = self.lg
        dlg = self.dlg
        count = self.count

        square_list = []
        for n in range(count):
            l = l0+n*dl
            lg = lg0+n*dlg
            x_shift = sv[0]+n*tv[0]
            y_shift = sv[1]+n*tv[1]
            square_list.append([-3.5+x_shift,-1+y_shift,1.5,2])
            square_list.append([-2+x_shift,(l-lg)/2+y_shift,4,lg])
            square_list.append([2+x_shift,-1+y_shift,1.5,2])

        return square_list

    def Pattern(self,pattern):
        pattern_dict = {'contact':self.Contact(),
                        'semiconductor':self.Semiconductor(),
                        'dielectric':self.Semiconductor(),
                        'gate':self.Gate(),
                        'gate_dualports':self.Gate_DualContact()}
        return pattern_dict[pattern]
    #  The semiconductor layer and the dielectric layer share the same pattern

    def WritePattern(self,filename,saving_directory=path.dirname(__file__)):
        for n in ['contact']:
            pattern = self.Pattern(n)
            directory = saving_directory+filename+'_'+n+'.xlsx'

            file = xlsxwriter.Workbook(directory)
            pattern_sheet = file.add_worksheet()

            pattern_sheet.write(0,0,'X_Start')  # Writing title
            pattern_sheet.write(0,1,'Y_Start')
            pattern_sheet.write(0,2,'X_Width')
            pattern_sheet.write(0,3,'Y_Width')

            for i in range(len(pattern)):
                for j in range(len(pattern[0])):
                    pattern_sheet.write(i+1,j,pattern[i][j])

            file.close()

        return

    def GeneratePatternSet(self,label,filename,saving_directory=path.dirname(__file__)):
        ptn = GenPTN.ptn()
        genlabel = GenLabel.Label()

        for n in ['contact','semiconductor','dielectric','gate','gate_dualports']:
            marking = genlabel.MakeMarking(n,0,0)
            if n == 'contact':
                text = genlabel.Text(label,6,0)
            else:
                text = []
            pattern = marking+text+self.Pattern(n)


            directory = saving_directory+filename+'_'+n+'.xlsx'

            file = xlsxwriter.Workbook(directory)
            pattern_sheet = file.add_worksheet()

            pattern_sheet.write(0,0,'X_Start')  # Writing title
            pattern_sheet.write(0,1,'Y_Start')
            pattern_sheet.write(0,2,'X_Width')
            pattern_sheet.write(0,3,'Y_Width')

            for i in range(len(pattern)):
                for j in range(len(pattern[0])):
                    pattern_sheet.write(i+1,j,pattern[i][j])

            file.close()

            ptn.PreviewPattern(directory,filename+'_'+n,saving_directory)
            ptn.ExcelToPTN(directory,filename+'_'+n,saving_directory,X_total=100.025,Y_total=20.025,DropletSpacing=self.DropletSpacing[n],X_unitcell=100,Y_unitcell=20)

        return





if __name__ =='__main__':
    tft = TFT(x=0,y=8,l=0.050,dl=0.010,w=1,dw=0,lg=0.5,dlg=0,x_distance=8,y_distance=0)
    #tft.WritePattern('Foundation','C:/Users/Majes/Desktop/Testing/')
    tft.GeneratePatternSet('2020-12-16','Foundation','C:/Users/Majes/Desktop/Testing/Foundation_test/')

    #ptn=GenPTN.ptn()  # 调用GenPTN模块的ptn函数
    # ptn.PreviewPattern('C:/Users/Majes/Desktop/Testing/Foundation_contact.xlsx','Whatever','C:/Users/Majes/Desktop/Testing/',X_unitcell=1000,Y_unitcell=1000,scale=10)
    #ptn.PreviewPattern('C:/Users/Majes/Desktop/Testing/Foundation_contact.xlsx','1','C:/Users/Majes/Desktop/Testing/',8000,1800,100)






