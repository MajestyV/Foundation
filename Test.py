import os
from Foundation import GenDevicePattern

saving_path = 'D:/OneDrive/OneDrive - The Chinese University of Hong Kong/Desktop/Testing/2021-03-29-pattern-(100-190)/'
saving_path_2 = 'D:/OneDrive/OneDrive - The Chinese University of Hong Kong/Desktop/Testing/2021-03-29-pattern-(100-190)-frontier/'

if not os.path.exists(saving_path):
    os.mkdir(saving_path)
else:
    os.remove(saving_path)
    os.mkdir(saving_path)

if not os.path.exists(saving_path_2):
    os.mkdir(saving_path_2)
else:
    os.remove(saving_path_2)
    os.mkdir(saving_path_2)

gdp =GenDevicePattern.Device()
# gdp.Resistor_on_PET('2021-03-05','2021-03-05',saving_path,w_top=1,dw_top=0.1,w_bottom=1,dw_bottom=0.1,num_device=6,X_unitcell=60,Y_unitcell=20)
gdp.TFT_on_SiO('2021-03-29','2021-03-29',saving_path,l=0.1,dl=0.01,w=1)
gdp.TFT_on_SiO_2('2021-03-29','2021-03-29',saving_path_2,l=0.1,dl=0.01,w=1,wg=0.25)
