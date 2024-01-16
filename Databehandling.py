import numpy as np
import matplotlib.pyplot as plt
import csv

#-----------------Mätning1------------------------------------
Spänning1_1_file = r'./Mätningar/Ångström_1/Spänning1.csv'
Spänning1_2_file = r'./Mätningar/Ångström_1/Spänning2.csv'
Temperatur1_1_file = r'./Mätningar/Ångström_1/Temperatur1.csv'
Temperatur1_2_file = r'./Mätningar/Ångström_1/Temperatur2.csv'
#-----------------Mätning2------------------------------------
Spänning2_1_file = r'./Mätningar/Ångström_2/Spänning1.csv'
Spänning2_2_file = r'./Mätningar/Ångström_2/Spänning2.csv'
Temperatur2_1_file = r'./Mätningar/Ångström_2/Temperatur1.csv'
Temperatur2_2_file = r'./Mätningar/Ångström_2/Temperatur2.csv'
#-----------------Mätning2------------------------------------
Spänning3_1_file = r'./Mätningar/Ångström_3/Spänning1.csv'
Spänning3_2_file = r'./Mätningar/Ångström_3/Spänning2.csv'
Temperatur3_1_file = r'./Mätningar/Ångström_3/Temperatur1.csv'
Temperatur3_2_file = r'./Mätningar/Ångström_3/Temperatur2.csv'

class Data:

    def __init__(self, data, Mätintervall, start=0):
        self.useful_data_start = start
        self.datadict = {}
        self.datadict['Time'] = []
        self.datadict['Amplitude'] = []
        with open(data, 'r', encoding='utf-8') as file:
            for row in file:
                if row[0].isnumeric():
                    r = row.split(';')
                    self.datadict['Time'].append(int(r[0])*Mätintervall)
                    self.datadict['Amplitude'].append(float('.'.join(r[1][:-1].split(','))))
        return
    
    def t(self):
        return self.datadict['Time'][self.useful_data_start:]
    
    def a(self):
        return self.datadict['Amplitude'][self.useful_data_start:]
    
    def get_frequency(self):
        x, y = np.array(self.t()), np.array(self.a())
        Freq_Amplitudes = np.abs(np.fft.fft(y))
        Freq = np.fft.fftfreq(len(x), x[1]-x[0])
        FFT = {}
        for i in range(len(Freq)):
            FFT[np.abs(Freq_Amplitudes[i])] = Freq[i]
        sorted_list = sorted(FFT.items(), key = lambda x:-x[0])
        # return abs(FFT[sorted_list[-2][0]])
        for i in range(100):
            if sorted_list[i][1] > 0.0015:
                relevant_frequency = sorted_list[i][1]
                break
        return relevant_frequency

Temperatur1_1 = Data(Temperatur1_1_file, 5, 6000)
Temperatur1_2 = Data(Temperatur1_2_file, 5, 6000)
Temperatur2_1 = Data(Temperatur2_1_file, 2, 3750)
Temperatur2_2 = Data(Temperatur2_2_file, 2, 3750)
Temperatur3_1 = Data(Temperatur2_1_file, 2, 4000)
Temperatur3_2 = Data(Temperatur2_2_file, 2, 4000)
Temperaturer = [Temperatur1_1, Temperatur1_2, Temperatur2_1 ,Temperatur2_2, Temperatur3_1, Temperatur3_2]

print(Temperatur2_2.get_frequency())

fig, axs = plt.subplots(3, 1, figsize=(20, 10))
counter=0
for i in range(3):
    axs[i].grid()
    axs[i].scatter(Temperaturer[counter].t(), Temperaturer[counter].a(), color='black', s=2)
    counter+=1
    axs[i].scatter(Temperaturer[counter].t(), Temperaturer[counter].a(), color='red', s=2)
    counter+=1
plt.show()