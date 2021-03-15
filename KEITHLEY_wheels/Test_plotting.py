from KEITHLEY_wheels import Get_KEITHLEY_Data

gd = Get_KEITHLEY_Data.geda()

file = 'D:/Projects/PhaseTransistor/DataGallery/2021-01-31/vds-id-C120D10DS10-Vd3VSweep-VgUncontact.xls'

directory = 'D:/Projects/PhaseTransistor/DataGallery/2021-01-31/'
plotting_list = [[file,['Data','Append1','Append2','Append3','Append4']]]
plotting_list_origin = [[file,['Append4']]]

gd.Visualize(plotting_list_origin,'Output Characteristics',xlim=(-3,3),yunit='uA',color=['g'],yscale='log')