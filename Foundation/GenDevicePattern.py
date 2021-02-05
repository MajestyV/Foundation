from Foundation import TripleTerminal_TFT_PET
from Foundation import TripleTerminal_TFT_SiO

class Device:
    """ This function set is written as interface to call different device pattern modules."""

    def __init__(self):
        self.name = None

    def TFT_on_PET(self,label,filename,saving_directory,**kwargs):
        #tft = TripleTerminal_TFT.TriplePort_TFT(0,8,l=kwargs['l'],dl=kwargs['dl'],w=kwargs['w'],dw=kwargs['dw'],lg=kwargs['lg'],dlg=kwargs['dlg'],count=kwargs['count'],x_distance=kwargs['x_distance'],y_distance=kwargs['y_distance'],semiconductor_width=kwargs['semiconductor_width'])
        tft = TripleTerminal_TFT_PET.TFT(0, 8, **kwargs)
        # Setting the starting point of the device as (0,8) to prevent overlap between the device pattern and the labels.
        # Using **kwargs to packing all the variables as a dictionary for functions to read. In this case, there is no need to specify particular variable.
        tft.GeneratePatternSet(label,filename,saving_directory)
        return

    def TFT_on_SiO(self,label,filename,saving_directory,**kwargs):
        tft = TripleTerminal_TFT_SiO.TFT(0,8,**kwargs)
        tft.GeneratePatternSet(label,filename,saving_directory)
        return

if __name__ == '__main__':
    device = Device()
    device.TFT_on_PET('2020-12-16','testing','C:/Users/Majes/Desktop/Testing/testing/',l=0.050,dl=0.1,w=2,dw=0,lg=0.5,dlg=0,num_device=10,x_distance=8,y_distance=0)