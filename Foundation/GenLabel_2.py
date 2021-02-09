import xlrd
# import xlsxwriter
import numpy as np
import os
from os import path
from Foundation import CharacterLibrary
# from Foundation import GenPTN


class Label:
    """ Upgraded version of GenLabel code. """

    def __init__(self,**kwargs):
        self.markersize = kwargs['markersize'] if 'markersize' in kwargs else 5  # The size of the marker label
        self.marker_linewidth = kwargs['marker_linewidth'] if 'marker_linewidth' in kwargs else 0.05  # Line width in the marker label
        self.origin_size = kwargs['origin_size'] if 'origin_size' in kwargs else 0.05  # The size of the origin in the marker label

        self.fontsize = kwargs['fontsize'] if 'fontsize' in kwargs else 5  # The size of the letters
        self.fontwidth = self.fontsize*0.75
        self.linewidth = self.fontsize/16.0
        self.character_distance = kwargs['character_distance'] if 'character_distance' in kwargs else self.fontsize-self.fontwidth  # The absolute distance between characters
        self.distance = self.character_distance+self.fontwidth  # The distance between starting point of two neighborhood characters

        self.CharacterLibraryPath = kwargs['Library_path'] if 'Library_path' in kwargs else path.dirname(__file__)+'/'

    # Patterns of the alignment marker label
    def MarkerLabel_0(self,x=0,y=0):
        w = self.markersize
        l0 = self.marker_linewidth
        origin_size = self.origin_size
        pattern = []
        pattern.append([x,y,origin_size,origin_size])  # Origin
        pattern.append([x+0.4*w,y,l0,0.4*w])
        pattern.append([x+0.6*w,y,l0,0.4*w])
        pattern.append([x+0.4*w,y+0.6*w,l0,0.4*w])
        pattern.append([x+0.6*w,y+0.6*w,l0,0.4*w])
        pattern.append([x,y+0.4*w,0.4*w,l0])
        pattern.append([x,y+0.6*w,0.4*w,l0])
        pattern.append([x+0.6*w,y+0.4*w,0.4*w,l0])
        pattern.append([x+0.6*w,y+0.6*w,0.4*w,l0])
        return pattern

    def MarkerLabel_1(self,x=0,y=0):
        w = self.markersize
        pattern = []
        pattern.append([x+0.45*w,y,0.1*w,w])
        pattern.append([x,y+0.45*w,w,0.1*w])
        return pattern

    def MarkerLabel_2(self,x=0,y=0):
        w = self.markersize
        pattern = []
        pattern.append([x+0.1*w,y+0.1*w,0.2*w,0.2*w])
        pattern.append([x+0.7*w,y+0.1*w,0.2*w,0.2*w])
        pattern.append([x+0.1*w,y+0.7*w,0.2*w,0.2*w])
        pattern.append([x+0.7*w,y+0.7*w,0.2*w,0.2*w])
        return pattern

    def MarkerLabel_3(self,x=0,y=0):
        w = self.markersize
        l0 = self.marker_linewidth
        pattern = []
        pattern.append([x,y,w,l0])
        pattern.append([x,y,l0,w])
        pattern.append([x,y+w,w,l0])
        pattern.append([x+w,y,l0,w])
        return pattern

    # This function is designed to extract pattern information inside excel files into an array.
    def ExtractCharacterInfo(self,InfoFile=path.dirname(__file__)+'/CharacterLibrary/CharacterLibrary.xlsx'):
        character_data = xlrd.open_workbook(InfoFile)
        num_character = character_data.nsheets  # Number of characters
        character_list = character_data.sheet_names()  # Content of the characters
        character_dict = dict.fromkeys(character_list)

        for n in range(num_character):
            table = character_data.sheet_by_name(character_list[n])
            pattern = np.zeros((24,12))  # The resolution of the character is set to be 24*12
            for i in range(table.nrows):
                for j in range(table.ncols):
                    content = table.cell_value(i,j)  # Reading the information of the specific cell
                    if content == 1:
                        pattern[i][j] =1

            character_dict[character_list[n]] = pattern

        return character_dict

    # This function is designed to convert the pattern information to the character library file.
    def GenCharacterLibrary(self,InfoFile=path.dirname(__file__)+'/CharacterLibrary/CharacterLibrary.xlsx'):
        library_file = self.CharacterLibraryPath+'CharacterLibrary.py'

        if path.exists(library_file):
            print('--- Character library file already exists. ---')
            update = input('--- Do you wat to update library? (Y/N) ---')
            if update == 'Y':
                os.remove(library_file)
            else:
                return

        file = open(library_file,'w')
        file.write('class Data:\n'
                   '    """ This is the Character Library. """\n'
                   '\n'
                   '    def __init__(self):\n'
                   '        self.name = Data\n'
                   '\n')

        character_dict = self.ExtractCharacterInfo(InfoFile)
        character_list = list(character_dict.keys())

        for n in range(len(character_list)):
            file.write('    def Character_'+str(character_list[n])+'(self):\n'
                       '        return [')
            array = character_dict[character_list[n]]
            for i in range(array.shape[0]):
                if i == array.shape[0]-1:  # Last row of the pattern array
                    file.write(str(array[i]).replace(' ',', ')+']\n')
                else:
                    file.write(str(array[i]).replace(' ',', ')+', ')

            file.write('\n')

        file.close()

        return character_list

    # This part responsible for converting the array to actual pattern parameters used for printing.
    def Array_to_Pattern(self,array,x,y):
        l0 = self.linewidth
        nrow, ncol = array.shape
        pattern = []
        for i in range(ncol):
            for j in range(nrow):
                if array[j][i] == 1:
                    pattern.append([x+i*l0,y+j*l0,l0,l0])
        return pattern

    # This function is designed to call the pattern of marker labels.
    def Marker(self,marker_name,x,y):
        marker_pattern = {'0':self.MarkerLabel_0(x,y),
                          '1':self.MarkerLabel_1(x,y),
                          '2':self.MarkerLabel_2(x,y),
                          '3':self.MarkerLabel_3(x,y),
                          'contact':self.MarkerLabel_0(x,y),
                          'semiconductor':self.MarkerLabel_1(x,y),
                          'dielectric':self.MarkerLabel_2(x,y),
                          'gate':self.MarkerLabel_3(x,y),
                          'gate_dualports':self.MarkerLabel_3(x,y)}
        return marker_pattern[marker_name]

    # This function is designed to call the pattern parameters for any character.
    def Character(self,character,x,y):
        character_array = CharacterLibrary.Data()
        character_pattern = {'0': self.Array_to_Pattern(np.array(character_array.Character_0()), x, y),
                             '1': self.Array_to_Pattern(np.array(character_array.Character_1()), x, y),
                             '2': self.Array_to_Pattern(np.array(character_array.Character_2()), x, y),
                             '3': self.Array_to_Pattern(np.array(character_array.Character_3()), x, y),
                             '4': self.Array_to_Pattern(np.array(character_array.Character_4()), x, y),
                             '5': self.Array_to_Pattern(np.array(character_array.Character_5()), x, y),
                             '6': self.Array_to_Pattern(np.array(character_array.Character_6()), x, y),
                             '7': self.Array_to_Pattern(np.array(character_array.Character_7()), x, y),
                             '8': self.Array_to_Pattern(np.array(character_array.Character_8()), x, y),
                             '9': self.Array_to_Pattern(np.array(character_array.Character_9()), x, y),
                             'A': self.Array_to_Pattern(np.array(character_array.Character_A()), x, y),
                             'T': self.Array_to_Pattern(np.array(character_array.Character_T()), x, y),
                             'G': self.Array_to_Pattern(np.array(character_array.Character_G()), x, y),
                             '-': self.Array_to_Pattern(np.array(character_array.Character_Dash()), x, y),
                             ' ': self.Array_to_Pattern(np.array(character_array.Character_Blank()), x, y)}
        return character_pattern[character]

    # Pattern writing modules
    def Text(self,text,x=0,y=0):
        d = self.distance

        text_pattern = []
        i = 0
        for letter in text:
            text_pattern = text_pattern+self.Character(letter,x+i*d,y)
            i = i+1

        return text_pattern

if __name__=='__main__':
    label = Label()
    #print(label.ExtractCharacterInfo()['A'])
    #print(label.Character('A',0,0))
    label.GenCharacterLibrary()