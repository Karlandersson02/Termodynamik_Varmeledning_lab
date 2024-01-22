import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

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

    def __init__(self, data, mätintervall, start=0, end=-1):
        self.data_start = start//mätintervall
        self.data_end = end//mätintervall
        self.datadict = {}
        self.datadict['Time'] = []
        self.datadict['Amplitude'] = []
        self.mätintervall = mätintervall
        self.peaks = []
        with open(data, 'r', encoding='utf-8') as file:
            for row in file:
                if row[0].isnumeric():
                    r = row.split(';')
                    self.datadict['Time'].append(int(r[0])*self.mätintervall)
                    self.datadict['Amplitude'].append(float('.'.join(r[1][:-1].split(','))))
        
        self.minindices = find_peaks(-np.array(self.a()), distance=int(0.9/self.get_frequency()/self.mätintervall))[0]
        self.maxindices = find_peaks(self.a(), distance=int(0.9/self.get_frequency()/self.mätintervall))
        return
    
    def t(self):
        return self.datadict['Time'][self.data_start:self.data_end]
    
    def a(self):
        return self.datadict['Amplitude'][self.data_start:self.data_end]
    
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
    
    def get_max_peaks(self):
        if self.peaks != []:
            return self.peaks
        self.peaks = []
        for index in self.maxindices:
            self.peaks.append((self.t()[index] ,self.a()[index]))
        return self.peaks
    
    def get_mini_peaks(self):
        peaks = []
        for index in self.minindices:
            peaks.append((self.t()[index], self.a()[index]))
        return peaks
    
    def get_Amplitude_mean(self):
        amps = [self.a()[self.maxindice[i]]-self.a()[self.minindice[i]] for i in range(len())]
        mean = sum(amps)/len(amps)
        return mean


class Measurement:

    def __init__(self, data1, data2, Mätintervall, start=0, end=-1):
        self.termoelement1 = Data(data1, Mätintervall, start, end)
        self.termoelement2 = Data(data2, Mätintervall, start, end)
        #print(len(self.termoelement1.get_mini_peaks()[0]), len(self.termoelement2.get_mini_peaks()[0]))
        print(len(self.termoelement1.get_max_peaks()), len(self.termoelement2.get_max_peaks()))
        self.length = 0.15
        
        self.wave_info = {'Par_'+str(i): 
                          {'t_ij': self.termoelement2.get_max_peaks()[i][0]-self.termoelement1.get_max_peaks()[i][0],}
                            for i in range(len(self.termoelement2.get_max_peaks()))}

    def get_mean(self):
        times = [self.wave_info[par]['t_ij'] for par in self.wave_info]
        return sum(times)/len(times)
    
    def get_damp(self):
        return self.termoelement1.get_Amplitude_mean()/self.termoelement2.get_Amplitude_mean()
    
    def get_alpha(self):
        return np.log(self.get_damp())/self.length
    
        

Temperatur1_1 = Data(Temperatur1_1_file, 5, 6000)
Temperatur1_2 = Data(Temperatur1_2_file, 5, 6000)
Temperatur2_1 = Data(Temperatur2_1_file, 2, 3750)
Temperatur2_2 = Data(Temperatur2_2_file, 2, 3750)
Temperatur3_1 = Data(Temperatur3_1_file, 2, 3000, 56000)
Temperatur3_2 = Data(Temperatur3_2_file, 2, 3000, 56000)
Temperaturer = [Temperatur1_1, Temperatur1_2, Temperatur2_1 ,Temperatur2_2, Temperatur3_1, Temperatur3_2]

Measurement1 = Measurement(Temperatur1_1_file, Temperatur1_2_file, 5, 6000)
Measurement2 = Measurement(Temperatur2_1_file, Temperatur2_2_file, 2, 3750)
Measurement3 = Measurement(Temperatur3_1_file, Temperatur3_2_file, 2, 4000)
# print(Measurement1.get_mean())
# print(Measurement2.get_mean())
# print(Measurement3.get_mean())

fig, axs = plt.subplots(3, 1, figsize=(20, 10))
counter=0
colors = 200*['red', 'green', 'yellow']
print(Measurement1.get_mean())

