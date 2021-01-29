import xlsxwriter
from os import  path
from Foundation import GenPTN
from Foundation import GenLabel

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
        self.count = kwargs['num_device'] if 'num_device' in kwargs else 10  # Number of devices in one pattern set, default =10
        self.dx = kwargs['x_distance'] if 'x_distance' in kwargs else 3  # Distance between devices in x-axis, default = 3mm
        self.dy = kwargs['y_distance'] if 'y_distance' in kwargs else 0  # Distance between devices in y-axis, default = 0
        self.w_semi = kwargs['semiconductor_width'] if 'semiconductor_width' in kwargs else 4  # Width of the semiconductor and dielectric layer
        # self.device_size = kwargs['device_size'] if 'device_size' in kwargs else 8  # The length of one size of the device, regarding the device is square as default

        self.shift_vec = [x + 3.5, y + 3.5]  # Vector for shifting calculated coordinates to the desired starting point
        self.translation_vec = [self.dx, self.dy]  # Vector for translating one device to a set of devices

        # The following part is written to determining the droplet spacing setting used to print each layer
        layer_list = ('contact', 'semiconductor', 'dielectric', 'gate')
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