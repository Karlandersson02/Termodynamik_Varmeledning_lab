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

    def __init__(self, data, Mätintervall):
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
        return self.datadict['Time']
    
    def a(self):
        return self.datadict['Amplitude']

Temperatur1_1 = Data(Temperatur1_1_file, 5)
Temperatur1_2 = Data(Temperatur1_2_file, 5)
Temperatur2_1 = Data(Temperatur2_1_file, 2)
Temperatur2_2 = Data(Temperatur2_2_file, 2)
Temperatur3_1 = Data(Temperatur2_1_file, 2)
Temperatur3_2 = Data(Temperatur2_2_file, 2)

def Oscillation_Frequency(x, y):
    x, y = np.array(x), np.array(y)
    Freq_Amplitudes = np.abs(np.fft.fft(y))
    Freq = np.fft.fftfreq(len(x), x[1]-x[0])
    FFT = {}
    for i in range(len(Freq)):
        FFT[np.abs(Freq_Amplitudes[i])] = Freq[i]
    sorted_list = sorted(FFT.items(), key = lambda x:x[0])
    return Freq, Freq_Amplitudes, FFT[sorted_list[-2][0]]

Freq, Freq_Amplitudes, Frequency = Oscillation_Frequency(Temperatur1_1.df['Time'][2500:], Temperatur1_1.df['Y'][2500:])