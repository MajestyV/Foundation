import xlrd
import re
import matplotlib.pyplot as plt

file_name = 'D:/Projects/PhaseTransistor/DataGallery/2020-12-11/G3C90-Gminus200V-50V-Sweep-20.xls'

data = xlrd.open_workbook(file_name)

sheet_list = data.sheet_names()

data_sheets = []
for n in sheet_list:
    #if n == 'Data' or n[0:6] == 'Append':
    if n == 'Data' or ('Append' in n):
        data_sheets.append(n)

#for n in data_sheets:
    #table = data.sheet_by_name(data_sheets[n])
    #for m in range(table.nrows):
        #if m == 0:

#table0 = data.sheet_by_name('Data')
#parameters = tuple(table0.row_values(0))  # Extracting the parameter list and transforming it to tuple.
#data_dict = dict.fromkeys(parameters)

#for n in range(table0.ncols):
    #testing_result = table0.col_values(n)
    #del testing_result[0]  # Deleting the name of parameters in the list.
    #data_dict[parameters[n]] = testing_result

total_data_dict = dict.fromkeys(tuple(data_sheets))  # The input of dict.fromkeys is tuple.
# The following loop is written to extract all the testing results from ever sheet.
# And then, distributing them to their corresponding key in the total_data_dict.
for n in data_sheets:
    testing_result = data.sheet_by_name(n)
    parameters = testing_result.row_values(0)  # Extracting the parameter names from the first row of the sheet.
    data_dict = dict.fromkeys(parameters)
    for m in range(testing_result.ncols):
        result = testing_result.col_values(m)
        del result[0]  # Deleting the name of parameters from the test data.
        data_dict[parameters[m]] = result

    total_data_dict[n] = data_dict



#for n in range(table0.nrows):
    #if n == 0:
        #data_dict = {table0.row_values(n)[m]:[] for m in range(len(table0.row_values(n)))}
    #else:
        #for m in range(len(table0.row_values(n))):
            #data_dict[table0.row_values(0)[m]].append(table0.row_values(n)[m])

print(sheet_list)
print(data_sheets)
#print(data_dict['GateI'])
#print(table0.col_values(0))
#print(total_data_dict)
print(total_data_dict['Append5']['DrainI'])

for n in data_sheets:
    if n == 'Data':
        label = 'loop 1'
    else:
        #index_set = set(n)-set('Append')  # 利用集合的不重复特性来提取测试序号
        #index_list = list(index_set)
        #index = int(''.join(index_list))
        index = re.sub(r'\D',"",n)
        label = 'loop '+str(int(index)+1)

    plt.plot(total_data_dict[n]['DrainV'],total_data_dict[n]['DrainI'], label=label)
    plt.legend(loc='best')

#print(index_list)
print(index)