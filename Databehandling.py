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
        self.peaks = {}
        self.minpeaks = {}
        with open(data, 'r', encoding='utf-8') as file:
            for row in file:
                if row[0].isnumeric():
                    r = row.split(';')
                    self.datadict['Time'].append(int(r[0])*self.mätintervall)
                    self.datadict['Amplitude'].append(float('.'.join(r[1][:-1].split(','))))
        
        self.minindices = find_peaks(-np.array(self.a()), distance=int(0.9/self.get_frequency()/self.mätintervall))[0]
        self.maxindices = find_peaks(self.a(), distance=int(0.9/self.get_frequency()/self.mätintervall))[0]
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
        if self.peaks != {}:
            return self.peaks
        self.peaks['T']=[]
        self.peaks['A']=[]
        for index in self.maxindices:
            self.peaks['T'].append(self.t()[index])
            self.peaks['A'].append(self.a()[index])
        return self.peaks
    
    def get_mini_peaks(self):
        if self.minpeaks != {}:
            return self.minpeaks
        self.minpeaks['T']=[]
        self.minpeaks['A']=[]
        for index in self.minindices:
            self.minpeaks['T'].append(self.t()[index])
            self.minpeaks['A'].append(self.a()[index])
        return self.minpeaks
    
    def get_Amplitude_list(self):
        amps = np.array([self.a()[self.maxindices[i]]-self.a()[self.minindices[i]] for i in range(len())])
        #mean = sum(amps)/len(amps)
        return amps/2


class Measurement:

    def __init__(self, data1, data2, Mätintervall, start=0, end=-1):
        self.termoelement1 = Data(data1, Mätintervall, start, end)
        self.termoelement2 = Data(data2, Mätintervall, start, end)
        self.length = 0.1
#        
#        self.wave_info = {'Par_'+str(i): 
#                          {'t_ij': self.termoelement2.get_max_peaks()[i][0]-self.termoelement1.get_max_peaks()[i][0],}
#                            for i in range(len(self.termoelement2.get_max_peaks()))}
#
    def get_mean(self):
        times = [self.wave_info[par]['t_ij'] for par in self.wave_info]
        return sum(times)/len(times)
    
    def get_damp(self):
        ampdiff = self.termoelement1.get_Amplitude_mean()/self.termoelement2.get_Amplitude_mean()
        return sum(ampdiff)/len(ampdiff)
    
    def get_alpha(self):
        return np.log(self.get_damp())/self.length
    
        

Temperatur1_1 = Data(Temperatur1_1_file, 5, 6000)
Temperatur1_2 = Data(Temperatur1_2_file, 5, 6000)
Temperatur2_1 = Data(Temperatur2_1_file, 2, 3600)
Temperatur2_2 = Data(Temperatur2_2_file, 2, 3600)
Temperatur3_1 = Data(Temperatur3_1_file, 2, 2750, 56000)
Temperatur3_2 = Data(Temperatur3_2_file, 2, 2750, 56000)
Temperaturer = [Temperatur1_1, Temperatur1_2, Temperatur2_1 ,Temperatur2_2, Temperatur3_1, Temperatur3_2]

#Measurement1 = Measurement(Temperatur1_1_file, Temperatur1_2_file, 5, 6000)
#Measurement2 = Measurement(Temperatur2_1_file, Temperatur2_2_file, 2, 3750)
#Measurement3 = Measurement(Temperatur3_1_file, Temperatur3_2_file, 2, 4000)
# print(Measurement1.get_mean())
# print(Measurement2.get_mean())
# print(Measurement3.get_mean())
print((len(Temperatur1_1.get_max_peaks()['T']), len(Temperatur1_1.get_mini_peaks()['T'])))
print((len(Temperatur1_2.get_max_peaks()['T']), len(Temperatur1_2.get_mini_peaks()['T'])))
print((len(Temperatur2_2.get_max_peaks()['T']), len(Temperatur2_2.get_mini_peaks()['T'])))
print((len(Temperatur2_1.get_max_peaks()['T']), len(Temperatur2_1.get_mini_peaks()['T'])))
print((len(Temperatur3_1.get_max_peaks()['T']), len(Temperatur3_1.get_mini_peaks()['T'])))
print((len(Temperatur3_2.get_max_peaks()['T']), len(Temperatur3_2.get_mini_peaks()['T'])))
fig, axs = plt.subplots(3, 1, figsize=(20, 10))
counter=0
colors = 200*['red', 'green', 'yellow']
#print(Measurement1.get_mean())
axs[0].plot(Temperatur1_1.t(), Temperatur1_1.a())
axs[0].plot(Temperatur1_2.t(), Temperatur1_2.a())
axs[0].scatter(Temperatur1_1.get_max_peaks()['T'], Temperatur1_1.get_max_peaks()['A'])
axs[0].scatter(Temperatur1_2.get_max_peaks()['T'], Temperatur1_2.get_max_peaks()['A'])

axs[1].plot(Temperatur2_1.t(), Temperatur2_1.a())
axs[1].plot(Temperatur2_2.t(), Temperatur2_2.a())
axs[1].scatter(Temperatur2_1.get_max_peaks()['T'], Temperatur2_1.get_max_peaks()['A'])
axs[1].scatter(Temperatur2_2.get_max_peaks()['T'], Temperatur2_2.get_max_peaks()['A'])

axs[2].plot(Temperatur3_1.t(), Temperatur3_1.a())
axs[2].plot(Temperatur3_2.t(), Temperatur3_2.a())
axs[2].scatter(Temperatur3_1.get_max_peaks()['T'], Temperatur3_1.get_max_peaks()['A'])
axs[2].scatter(Temperatur3_2.get_max_peaks()['T'], Temperatur3_2.get_max_peaks()['A'])
plt.show()