import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from Spänningsomvandlare import Thermocouple
to_temp = Thermocouple.mv_to_typek
to_volt = Thermocouple.typek_to_mv

Tjock_kall_file = r'./Mätningar/Tjock_koppar/Tjockkoppar_kallt_till_luft.csv'
Tjock_varm_file = r'./Mätningar/Tjock_koppar/Tjockkoppar_varmt_till_luft_1.csv'
Tunn_kall_file = r'./Mätningar/Tunn_koppar/Koppar_kallt_till_luft_1.csv'
Tunn_varm_file = r'./Mätningar/Tunn_koppar/Koppar_varmt_till_luft_1.csv'


class EData:
    def __init__(self, file):
        self.datadict = {}
        self.datadict['Time'] = []
        self.datadict['Voltage'] = []
        self.refmv = to_volt(21) # Referensspänningen i mV (spänningen som motsvarar 21 grader celsius med referenspunkt 0 grader celsius)
        self.mätintervall = 61/117
        with open(file, 'r', encoding='utf-8') as file:
            for row in file:
                if row[0].isnumeric():
                    r = row.split(';')
                    self.datadict['Time'].append(int(r[0])*self.mätintervall)
                    self.datadict['Voltage'].append(float('.'.join(r[1][:-1].split(','))))
        if self.datadict['Time'][0] != 0:
            t_0 = self.datadict['Time'][0]
            for i in range(len(self.datadict['Time'])):
                self.datadict['Time'][i] = self.datadict['Time'][i] - t_0
    
    def V(self):
        return self.datadict['Voltage']
    
    def T(self):
        return self.datadict['Time']
    
    def K(self):
        temp = []
        for volt in self.V():
            temp.append(to_temp(1000*volt+self.refmv))
        return temp
    
    def __len__(self):
        return len(self.T())

class Comparison:
    def __init__(self, file1, file2):
        self.varm = EData(file1)
        self.kall = EData(file2)
        self.datadict = {}
        self.datadict['varm'] = {}
        self.datadict['varm']['temp']=[]

        self.datadict['kall'] = {}
        self.datadict['kall']['temp']=[]

        for temp in self.varm.K():
            self.datadict['varm']['temp'].append(temp)
        self.datadict['varm']['time']=self.varm.T()[:len(self.datadict['varm']['temp'])]

        for temp2 in self.kall.K():
            if temp2 > 21-(max(self.datadict['varm']['temp'])-21): # Spänningen som motsvarar en -53,5 grader Celsius minskning från 21 grader Celsius
                self.datadict['kall']['temp'].append(temp2)
        self.datadict['kall']['time']=self.kall.T()[:len(self.datadict['kall']['temp'])]
        if len(self.t_varm())>len(self.t_kall()):
            self.datadict['varm']['time'] = self.datadict['varm']['time'][:len(self.t_kall())]
            self.datadict['varm']['temp'] = self.datadict['varm']['temp'][:len(self.t_kall())]
        if len(self.t_varm())<len(self.t_kall()):
            self.datadict['kall']['time'] = self.datadict['kall']['time'][:len(self.t_varm())]
            self.datadict['kall']['temp'] = self.datadict['kall']['temp'][:len(self.t_varm())]
    
    def t_kall(self):
        return self.datadict['kall']['time']
    
    def t_varm(self):
        return self.datadict['varm']['time']
    
    
    def Temp_kall(self):
        return self.datadict['kall']['temp']
    
    def Temp_varm(self):
        return self.datadict['varm']['temp']




Tjock_kall = EData(Tjock_kall_file)
Tjock_varm = EData(Tjock_varm_file)
Tunn_kall = EData(Tunn_kall_file)
Tunn_varm = EData(Tunn_varm_file)
Tjock = Comparison(Tjock_varm_file, Tjock_kall_file)
Tunn = Comparison(Tunn_varm_file, Tunn_kall_file)

#print(Tjock.Temp_kall()[0], 21-Tjock.Temp_kall()[0])
#print(Tjock.Temp_varm()[0], Tjock.Temp_varm()[0]-21)
#
#print(Tunn.Temp_kall()[0], 21-Tunn.Temp_kall()[0])
#print(Tunn.Temp_varm()[0], Tunn.Temp_varm()[0]-21)
matplotlib.rcParams.update({'font.size': 16})
fig, axs = plt.subplots(2, 1, figsize=(20, 10))
plt.subplots_adjust(hspace=0.5)
axs[0].plot(Tjock.t_varm(), Tjock.Temp_varm(), color = 'red', label = 'Varma')
axs[0].plot(Tjock.t_kall(), Tjock.Temp_kall(), color = 'blue', label = 'Kalla')
axs[0].scatter(Tjock.t_varm()[-1], Tjock.Temp_varm()[-1], s=80, color = 'red', label = f'Temperatur = {Tjock.Temp_varm()[-1]:.3} °C')
axs[0].scatter(Tjock.t_kall()[-1], Tjock.Temp_kall()[-1], s=80, color = 'blue', label = f'Temperatur = {Tjock.Temp_kall()[-1]:.3} °C')
axs[0].plot(Tjock.t_varm(), [21]*len(Tjock.t_varm()), linestyle = '--', label = '21°C', color = 'black')
axs[0].grid()
axs[0].set_xlabel('Tid [s]')
axs[0].set_ylabel('Temperatur [°C]')
axs[0].set_title('Tjock')
axs[0].legend(fontsize='12')

axs[1].plot(Tunn.t_varm(), Tunn.Temp_varm(), color = 'red', label = 'Varma')
axs[1].plot(Tunn.t_kall(), Tunn.Temp_kall(), color = 'blue', label = 'Kalla')
axs[1].scatter(Tunn.t_varm()[-1], Tunn.Temp_varm()[-1], s=80, color = 'red', label = f'Temperatur = {Tunn.Temp_varm()[-1]:.3} °C')
axs[1].scatter(Tunn.t_kall()[-1], Tunn.Temp_kall()[-1], s=80, color = 'blue', label = f'Temperatur = {Tunn.Temp_kall()[-1]:.3} °C')
axs[1].plot(Tunn.t_varm(), [21]*len(Tunn.t_varm()), linestyle = '--', label = '21°C', color = 'black')
axs[1].grid()
axs[1].set_xlabel('Tid [s]')
axs[1].set_ylabel('Temperatur [°C]')
axs[1].set_title('Tunn')
axs[1].legend(fontsize='12')

plt.show()