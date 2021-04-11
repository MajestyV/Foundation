from os import path
from Foundation import GenPTN
from Foundation import GenLabel_2

default_directory = path.dirname(__file__)+'/'  # 设置默认的保存路径

class samples:
    "This function class is designed to generate coordinates of sample array for all sorts of Characterization."
    # All the units in this function class is [mm].

    def __init__(self,x=0,y=0,**kwargs):
        self.x = x  # Starting point of the pattern
        self.y = y

        self.row_index = ['A','B','C','D','E','F','G','H']
        self.column_index = ['1','2','3','4','5','6','7','8']
        self.label_size = kwargs['label_size'] if 'label_size' in kwargs else 1.5  # 样品编号的字体大小
        self.alignment_size = kwargs['alignment_size'] if 'alignment_size' in kwargs else 1  # 对准标记的大小

        self.array_size = kwargs['array_size'] if 'array_size' in kwargs else (4,4)  # Size of the sample array, 格式: (行数, 列数)
        self.width_sample = kwargs['sample_width'] if 'sample_width' in kwargs else 10.0  # Size of one sample region

        # 待测样品薄膜的信息，eg. [8,9,10] - 三层样品薄膜，每层的大小分别是8mm*8mm, 9mm*9mm, 10mm*10mm
        self.width_film_list = kwargs['film_list'] if 'film_list' in kwargs else [8]
        self.num_film = len(self.width_film_list)

        # 定义用于preview pattern的BMP图中器件的放大倍数
        self.scale = kwargs['preview_scale'] if 'preview_scale' in kwargs else 40

    def Marker(self):
        size = self.array_size  # 样本阵列的大小
        width = self.width_sample  # 一个样本区域的宽
        height = self.width_sample+self.label_size  # 一个样本区域的高
        l_alignment = self.alignment_size
        w_label = self.label_size

        genlabel = GenLabel_2.Label(fontsize=w_label,character_distance=0.2)  # 调用生成标记图案坐标信息的包

        square_list = []
        for i in range(size[0]):
            for j in range(size[1]):
                x_shift = j*width
                y_shift = i*height
                square_list.append([x_shift,y_shift,l_alignment,0.05])  # 左上角标记
                square_list.append([x_shift,y_shift,0.05,l_alignment])
                square_list.append([width-0.05+x_shift,height-l_alignment+y_shift,0.05,l_alignment])  # 右下角标记
                square_list.append([width-l_alignment+x_shift,height-0.05+y_shift,l_alignment,0.05])

                # 生成样本编号的图案信息
                x_label = width/2.0-(3*w_label/4.0+0.1)+x_shift  # 计算样本编号的起始点
                y_label = width+y_shift
                text = genlabel.Text(self.row_index[i]+self.column_index[j],x_label,y_label)
                square_list = square_list+text

        return square_list

    def GeneratePatternSet(self,filename,saving_directory=default_directory):
        size = self.array_size
        w = self.width_sample
        h = self.width_sample+self.label_size

        ptn = GenPTN.ptn()
        excel_file = ptn.WritePattern(self.Marker(),filename+'_label_'+str(w)+'mm',saving_directory)
        ptn.PreviewPattern(excel_file,filename+'_label_'+str(w)+'mm',saving_directory,X_unitcell=int(w*size[1]*self.scale),Y_unitcell=int(h*size[0]*self.scale),scale=self.scale)  # BMP的行列像素个数都必须是整数
        ptn.ExcelToPTN(excel_file,filename+'_label_'+str(w)+'mm',saving_directory,X_total=w*size[1]+0.025,Y_total=h*size[0]+0.025,X_unitcell=w*size[1],Y_unitcell=h*size[0])

        for n in range(self.num_film):
            w_film = self.width_film_list[n]
            square_list = [[(w-w_film)/2.0,(w-w_film)/2.0,w_film,w_film]]
            excel_file = ptn.WritePattern(square_list,filename+'_layer_'+str(w_film)+'mm',saving_directory)
            ptn.PreviewPattern(excel_file,filename+'_layer_'+str(w_film)+'mm',saving_directory,X_unitcell=int(w*size[1]*self.scale),Y_unitcell=int(h*size[0]*self.scale),scale=self.scale)
            ptn.ExcelToPTN(excel_file,filename+'_layer_'+str(w_film)+'mm',saving_directory,X_total=w+0.025,Y_total=h+0.025,X_unitcell=w,Y_unitcell=h)

        return


if __name__ == '__main__':
    sample_array = samples()

    saving_directory = 'D:/OneDrive/OneDrive - The Chinese University of Hong Kong/Desktop/Testing/'

    ptn = GenPTN.ptn()
    excel_file = ptn.WritePattern(sample_array.Marker(),'sample_test',saving_directory)
    ptn.PreviewPattern(excel_file,'sample_test',saving_directory,X_unitcell=2000,Y_unitcell=2000,scale=40)