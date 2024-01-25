import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import FormatStrFormatter
from scipy.signal import find_peaks
from Spänningsomvandlare import Thermocouple
to_temp = Thermocouple.mv_to_typek
to_volt = Thermocouple.typek_to_mv

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

class Termoelement:

    def __init__(self, data, mätintervall, start=0, end=-1):
        self.data_start = start//mätintervall
        self.data_end = end//mätintervall
        self.datadict = {}
        self.datadict['Time'] = []
        self.datadict['Amplitude'] = []
        self.mätintervall = mätintervall
        self.peaks = {}
        self.minpeaks = {}
        self.ref_temp = 21
        self.Temperature = []
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
        if self.Temperature==[]:
            ref_volt = to_volt(self.ref_temp)
            self.Temperature =[to_temp(volt*1e3+ref_volt) for volt in self.datadict['Amplitude'][self.data_start:self.data_end]]
        return self.Temperature
    
    def get_frequency(self):
        x, y = np.array(self.t()), np.array(self.a())
        Freq_Amplitudes = np.abs(np.fft.fft(y))
        Freq = np.fft.fftfreq(len(x), x[1]-x[0])
        FFT = {}
        for i in range(len(Freq)):
            FFT[np.abs(Freq_Amplitudes[i])] = Freq[i]
        sorted_list = sorted(FFT.items(), key = lambda x:-x[0])
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
        amps = np.array([self.a()[self.maxindices[i]]-self.a()[self.minindices[i]] for i in range(len(self.minindices))])
        return amps/2


class Measurement:

    def __init__(self, data1, data2, Mätintervall, start=0, end=-1):
        self.termoelement1 = Termoelement(data1, Mätintervall, start, end)
        self.termoelement2 = Termoelement(data2, Mätintervall, start, end)
        self.length = 0.1
        self.c = 418.68
        self.rho = 8.96e6*1e-3

    def get_mean(self):
        times = [self.wave_info[par]['t_ij'] for par in self.wave_info]
        return sum(times)/len(times)
    
    def get_beta_prime(self): #beta/w
        return (np.array(self.termoelement2.get_max_peaks()['T']) - np.array(self.termoelement1.get_max_peaks()['T']))/self.length
    
    def get_damp(self):
        damp = self.termoelement1.get_Amplitude_list()/self.termoelement2.get_Amplitude_list()
        return damp
    
    def get_alpha(self):
        return np.log(self.get_damp())/self.length
    
    def get_conductivity(self):
        if not hasattr(self, 'lambdas'):
            alphas = self.get_alpha()
            beta_primes = self.get_beta_prime()
            self.lambdas = []
            for alpha in alphas:
                for beta_prime in beta_primes:
                    self.lambdas.append(self.c*self.rho/2/alpha/beta_prime)
        return self.lambdas
    
    def get_mean_conductivity(self):
        return sum(self.get_conductivity())/len(self.get_conductivity())

    def get_standard_error(self):
        lambdas = self.get_conductivity()
        lambda_mean = self.get_mean_conductivity()
        n = len(lambdas)
        return np.sqrt(sum((lambdas-lambda_mean)**2))/n
    
    def get_peak_range(self, Antal_peaks=20, guess = 'asdf'):
        
        peaks1 = self.termoelement1.get_max_peaks()
        peaks2 = self.termoelement2.get_max_peaks()
        if guess == 'asdf':
            guess = (peaks1['T'][-1]-peaks1['T'][0])//2
        
        for i in range(1000):
            if guess+i in peaks1['T']:
                start_tid1 = guess+i
                start_index1 = self.termoelement1.t().index(start_tid1)
                slut_tid = peaks1['T'][peaks1['T'].index(start_tid1)+Antal_peaks]
                slut_index1 = self.termoelement1.t().index(slut_tid)
                break
        
        return (start_index1, slut_index1) 

class Measurements:
    def __init__(self):
        self.Measurement1 = Measurement(Spänning1_1_file, Spänning1_2_file, 5, 6000)
        self.Measurement2 = Measurement(Spänning2_1_file, Spänning2_2_file, 2, 3750)
        self.Measurement3 = Measurement(Spänning3_1_file, Spänning3_2_file, 2, 4000, -9350)

    def get_info(self):
        Conductivity1 = self.Measurement1.get_mean_conductivity()
        Conductivity2 = self.Measurement2.get_mean_conductivity()
        Conductivity3 = self.Measurement3.get_mean_conductivity()

        StandardError1 = self.Measurement1.get_standard_error()
        StandardError2 = self.Measurement2.get_standard_error()
        StandardError3 = self.Measurement3.get_standard_error()

        print('----------------------------------------------------------------')
        print(f'Measurement 1: Conductivity = {Conductivity1:.2f} with Standard Error = {StandardError1:.2f}.')
        print(f'Measurement 2: Conductivity = {Conductivity2:.2f} with Standard Error = {StandardError2:.2f}.')
        print(f'Measurement 3: Conductivity = {Conductivity3:.2f} with Standard Error = {StandardError3:.2f}.')
        print('----------------------------------------------------------------')

        return
    
    def plot_data(self, Selection = [1, 2, 3], Save=False):

        Data = []
        Mätningar = []
        Peak_range = []
        if 1 in Selection:
            Data.append(Measurements().Measurement1)
            Mätningar.append('(2V, 5min)')
            Peak_range.append(Measurements().Measurement1.get_peak_range(Antal_peaks=2))
        if 2 in Selection:
            Data.append(Measurements().Measurement2)
            Mätningar.append('(2V, 3min)')
            Peak_range.append(Measurements().Measurement2.get_peak_range(Antal_peaks=2))
        if 3 in Selection:
            Data.append(Measurements().Measurement3)
            Mätningar.append('(2V, 2min)')
            Peak_range.append(Measurements().Measurement3.get_peak_range(Antal_peaks=2))
        
        matplotlib.rcParams.update({'font.size': 16})
        fig, axs = plt.subplots(len(Selection), 1, figsize=(20,10))
        plt.subplots_adjust(hspace=0.7)
        for i in range(len(Data)):
            axs[i].set_title(f'Värmevåg {Mätningar[i]}')
            axs[i].plot(Data[i].termoelement1.t(), Data[i].termoelement1.a(), color = 'black', label='Termoelement 1')
            axs[i].plot(Data[i].termoelement2.t(), Data[i].termoelement2.a(), color = 'red', label='Termoelement 2')
            axs[i].set_ylabel(r'Temperatur [$^o$C]')
            axs[i].set_xlabel(r'Tid $[s]$')
            axs[i].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
            axs[i].xaxis.set_tick_params(labelsize=12)
            axs[i].yaxis.set_tick_params(labelsize=12)
            axs[i].grid()
            axs[i].legend(loc='upper left', fontsize=12)
        if Save==True:
            plt.savefig(r'.\Bilder\Experiment_all_data.pdf')
        plt.show()

        fig, axs = plt.subplots(len(Selection), 2, figsize=(20,10))
        plt.subplots_adjust(hspace=0.8)
        # matplotlib.axes.Axes.tick_params({'labelsize': 12})
        for i in range(len(Data)):
            axs[i][0].plot(Data[i].termoelement1.t()[Peak_range[i][0]:Peak_range[i][1]], Data[i].termoelement1.a()[Peak_range[i][0]:Peak_range[i][1]], color='black')
            axs[i][1].plot(Data[i].termoelement2.t()[Peak_range[i][0]:Peak_range[i][1]], Data[i].termoelement2.a()[Peak_range[i][0]:Peak_range[i][1]], color='red')
            axs[i][0].grid()
            axs[i][1].grid()
            if i == 0:
                 axs[i][0].set_title(f'Termoelement 1 närbilder \n {Mätningar[i]}')
                 axs[i][1].set_title(f'Termoelement 2 närbilder \n {Mätningar[i]}')
            else:
                axs[i][0].set_title(f'{Mätningar[i]}')
                axs[i][1].set_title(f'{Mätningar[i]}')
            axs[i][0].xaxis.set_tick_params(rotation=27.5, labelsize=12)
            axs[i][1].xaxis.set_tick_params(rotation=27.5, labelsize=12)
            axs[i][0].yaxis.set_tick_params(labelsize=12)
            axs[i][1].yaxis.set_tick_params(labelsize=12)
            axs[i][0].set_xlabel(r'Tid [s]')
            axs[i][0].set_ylabel(r'Temperatur [$^o$C]')
            axs[i][1].set_xlabel(r'Tid $[s]$')
            axs[i][1].set_ylabel(r'Temperatur [$^o$C]')
            axs[i][0].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
            axs[i][1].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        if Save==True:
            plt.savefig(r'.\Bilder\Experiment_utvald_data.pdf')
        plt.show()
        return

measurements = Measurements()
measurements.get_info()
measurements.plot_data(Save=True)
