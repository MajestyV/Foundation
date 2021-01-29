from Foundation import GenBMP
import numpy as np
import xlrd
import os
from os import path

class ptn:
    """ This script is designed to extract PTN file information. """

    def __init__(self):
        self.a = 1 # Useless line

    def GetPTNContent(self,file_path):
        file = open(file_path)
        line = file.readline()
        content = []
        while line:
            line_content = list(map(str, line.split('>')))
            content.append(line_content)
            line = file.readline()
        file.close()
        return content

    def PTN(self):
        self.PTN_Content = '<?xml version="1.0"?><!--Standalone Deposition Materials Printer Pattern File--><PatternFile>'

    # This function is designed to define the general configuration parameters of a PTN file.
    def PTN_GeneralConfig(self,Width,Height,LeaderBar=0,LeaderBarWidth=0,LeaderBarGap=0,DropletSpacing=25,LayerCount=1,LayerDelayInSeconds=0):
        content = "<GeneralConfig>"
        content = content+"<Left>0</Left><Top>0</Top>"
        content = content+"<Width>"+str(Width)+"</Width>"
        content = content+"<Height>"+str(Height)+"</Height>"
        content = content+"<UseReferenceCoordinates>False</UseReferenceCoordinates><XReference>0</XReference><YReference>0</YReference><XReferenceTile>0</XReferenceTile><YReferenceTile>0</YReferenceTile>"
        if LeaderBar == 0:
            content = content+"<UseLeaderBar>False</UseLeaderBar><LeaderBarWidth>0</LeaderBarWidth><LeaderBarGap>0</LeaderBarGap>"
        else:
            content = content+"<UseLeaderBar>False</UseLeaderBar><LeaderBarWidth>"+str(LeaderBarWidth)+"</LeaderBarWidth><LeaderBarGap>"+str(LeaderBarGap)+"</LeaderBarGap>"
        content = content+"<JetSpacing>"+str(DropletSpacing)+"</JetSpacing>"
        content = content+"<LayerCount>"+str(LayerCount)+"</LayerCount>"
        content = content+"<LayerDelayInSeconds>"+str(LayerDelayInSeconds)+"</LayerDelayInSeconds>"
        content = content+"</GeneralConfig>"

        self.PTN_Content = self.PTN_Content+content

        return content

    # This function is designed to define the parameters of a pattern unitcell.
    def PTN_Unitcell(self,Width,Height,XSpacing=0,YSpacing=0,MaxXCount=1,MaxYCount=1):
        content = "<PatternBlock>"
        content = content+"<Left>0</Left><Top>0</Top>"
        content = content+"<Width>"+str(Width)+"</Width>"
        content = content+"<Height>"+str(Height)+"</Height>"
        content = content+"<XSpacing>"+str(XSpacing)+"</XSpacing>"
        content = content+"<YSpacing>"+str(YSpacing)+"</YSpacing>"
        content = content+"<MaxXCount>"+str(MaxXCount)+"</MaxXCount>"
        content = content+"<MaxYCount>"+str(MaxYCount)+"</MaxYCount>"

        self.PTN_Content = self.PTN_Content+content

        return content

    # This function is designed to define the pattern.
    def PTN_Pattern(self,StartX,StartY,XWidth,YHeight):
        content = "<Drop>"
        content = content+"<StartX>"+str(StartX)+"</StartX>"
        content = content+"<StartY>"+str(StartY)+"</StartY>"
        content = content+"<XWidth>"+str(XWidth)+"</XWidth>"
        content = content+"<YHeight>"+str(YHeight)+"</YHeight>"
        content = content+"</Drop>"

        self.PTN_Content = self.PTN_Content+content

        return content

    def Save_PTN(self,file_name,saving_directory=path.dirname(__file__)):
        self.PTN_Content = self.PTN_Content+"</PatternBlock></PatternFile>"
        file_name = saving_directory+file_name+'.ptn'
        if os.path.exists(file_name):
            print('File existed, please rename the file or remove original file.')
            Rename = input('Do you want to rename the file? (Y/N)')
            if Rename == 'Y':
                New_name = input('Please enter new file name.')
                file_name = saving_directory+New_name+'.ptn'
                file = open(file_name, "a")
                file.write(self.PTN_Content)
                file.close()
            else:
                Cover = input('Do you want to cover the original file? (Y/N)')
                if Cover == 'Y':
                    file = open(file_name,'w')
                    file.write(self.PTN_Content)
                    file.close()
        else:
            file = open(file_name,"a")  # "a"-追加写入, "w"-覆盖写入, "r"-只读
            file.write(self.PTN_Content)
            file.close()

    # This function is for converting Excel file to PTN file.
    def ExcelToPTN(self,Excel_file,file_name,saving_directory=path.dirname(__file__),X_total=40.025,Y_total=40.025,DropletSpacing=20,layer=1,X_unitcell=40,Y_unitcell=40,x_count=1,y_count=1):
        self.PTN()
        self.PTN_GeneralConfig(X_total,Y_total,DropletSpacing=DropletSpacing,LayerCount=layer)
        self.PTN_Unitcell(X_unitcell,Y_unitcell,MaxXCount=x_count,MaxYCount=y_count)

        pattern_data = xlrd.open_workbook(Excel_file)
        table = pattern_data.sheet_by_index(0)
        title = []
        pattern_list = []
        for n in range(table.nrows):
            if n == 0:
                title.append(table.row_values(n))
            else:
                pattern_list.append(table.row_values(n))
        pattern = [[np.float(pattern_list[i][j]) for j in range(len(pattern_list[i]))] for i in range(len(pattern_list))]

        for i in range(len(pattern_list)):
            x0, y0, w, h = pattern_list[i]
            self.PTN_Pattern(np.float(x0),np.float(y0),np.float(w),np.float(h))

        self.Save_PTN(file_name,saving_directory)

        return pattern

    # Using GenBMP to generate a BMP picture to preview the pattern of a unitcell in the Excel file.
    def PreviewPattern(self,Excel_file,file_name,saving_directory=path.dirname(__file__),X_unitcell=8000,Y_unitcell=1800,scale=100):
        file_name = saving_directory+file_name+".bmp"

        pattern_data = xlrd.open_workbook(Excel_file)
        table = pattern_data.sheet_by_index(0)
        title = []
        pattern_list = []
        for n in range(table.nrows):
            if n == 0:
                title.append(table.row_values(n))
            else:
                pattern_list.append(table.row_values(n))
        pattern = [[int(np.float(pattern_list[i][j])*scale) for j in range(len(pattern_list[i]))] for i in range(len(pattern_list))]

        image = GenBMP.bmp(X_unitcell,Y_unitcell)
        image.gen_bmp_header()
        image.print_bmp_header()

        image.paint_bgcolor()

        for i in range(len(pattern)):
            x0, y0, w, h = pattern[i]
            image.paint_rect(x0, y0, w, h)

        image.save_image(file_name)

        return pattern



if __name__=='__main__':
    ptn = ptn()
    result = ptn.GetPTNContent("C:/Users/Majes/Desktop/Testing/Origin.ptn")
    print(result)

    ptn.PTN()
    ptn.PTN_GeneralConfig(10,10,DropletSpacing=20)
    ptn.PTN_Unitcell(5,5)
    ptn.PTN_Pattern(0,0,0.1,0.1)
    ptn.PTN_Pattern(0.1,0.1,0.1,0.1)
    ptn.PTN_Pattern(0.2,0.2,0.1,0.1)
    ptn.PTN_Pattern(0.3,0.3,0.1,0.1)
    ptn.Save_PTN('HeyThere',"C:/Users/Majes/Desktop/Testing/")