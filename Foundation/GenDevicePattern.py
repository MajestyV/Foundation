from Foundation import TripleTerminal_TFT_PET
from Foundation import TripleTerminal_TFT_SiO
from Foundation import TripleTerminal_TFT_SiO_2
from Foundation import Vertical_Resistor_PET
from Foundation import GenLabel_2
from Foundation import GenPTN
import xlsxwriter

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
        tft = TripleTerminal_TFT_SiO.TFT(0,5,**kwargs)
        tft.GeneratePatternSet(label,filename,saving_directory)
        return

    def TFT_on_SiO_2(self, label, filename, saving_directory, **kwargs):
        tft = TripleTerminal_TFT_SiO_2.TFT(0, 5, **kwargs)
        tft.GeneratePatternSet(label, filename, saving_directory)
        return

    def Resistor_on_PET(self,label,filename,saving_directory,**kwargs):
        resistor = Vertical_Resistor_PET.Resistor(0,5,**kwargs)
        resistor.GeneratePatternSet(label,filename,saving_directory)
        return

    def Merge(self,label,filename,saving_directory,**kwargs):
        tft1 = TripleTerminal_TFT_SiO.TFT(0,5,**kwargs)
        contact1 = tft1.Pattern('contact')
        semiconductor1 = tft1.Pattern('semiconductor')
        dielectric1 = tft1.Pattern('dielectric')
        tft2 = TripleTerminal_TFT_SiO_2.TFT(35,5,**kwargs)
        contact2 = tft2.Pattern('contact')
        semiconductor2 = tft2.Pattern('semiconductor')
        dielectric2 = tft2.Pattern('dielectric')

        ptn = GenPTN.ptn()
        genlabel = GenLabel_2.Label(markersize=3,fontsize=2,character_distance=0.2)

        pattern_dict = {'contact': contact1+contact2+genlabel.Marker('0',0,0)+genlabel.Text(label,3.5,0),
                        'semiconductor': semiconductor1+semiconductor2+genlabel.Marker('1',0,0),
                        'dielectric': dielectric1+dielectric2+genlabel.Marker('2',0,0)}

        scale=50
        for n in ['contact','semiconductor','dielectric']:
            directory = saving_directory + filename + '_' + n + '.xlsx'
            pattern = pattern_dict[n]

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

            ptn.PreviewPattern(directory, filename + '_' + n, saving_directory, X_unitcell=70*scale, Y_unitcell=15 * scale, scale=scale)
            ptn.ExcelToPTN(directory, filename + '_' + n, saving_directory, X_total=70 + 0.025,Y_total=15 + 0.025, X_unitcell=70,Y_unitcell=15)
        return


if __name__ == '__main__':
    device = Device()
    device.TFT_on_PET('2020-12-16','testing','C:/Users/Majes/Desktop/Testing/testing/',l=0.050,dl=0.1,w=2,dw=0,lg=0.5,dlg=0,num_device=10,x_distance=8,y_distance=0)