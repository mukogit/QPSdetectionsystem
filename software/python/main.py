import serial
import os
import datetime
import numpy as np

port = 'COM1'

teensy, data = None, None
baud = 2000000
voltage1_offset = 900 #measurement dep. value
voltage2_offset = 600 #measurement dep. value
pc = 0 				  #2@$\pi$@ phasecounter
phase_offset = 0 		  #phase offset    
pidiff = 6

teensy = serial.Serial(port, baudrate=baud)

directory = os.getcwd()
now = datetime.datetime.now()
filename = now.strftime('%y%m%d_%H%M%S')

path = ('{0}\\data\\{1}_data.csv'.format(directory, filename))
outfile = open(path, 'w+')
outfile.write('time,v1,v2,unwrapped phase,position\n')

data_acquisition = True

while data_acquisition:
    data = teensy.readline()
    data = data[0:-2].decode('utf-8')
    
    #extract time and voltages
    time = int(data[0:9]) / 1000000
    v1 = int(data[9:13])  #voltage at S@$_1$@
    v2 = int(data[13:17]) #voltage at S@$_2$@
    
    #offset around zero and normalize
    v1_lev = v1 - voltage1_offset
    v2_lev = v2 - voltage2_offset
    _sqrt = np.sqrt(v1_lev**2 + v2_lev**2)
    v1_norm = v1_lev / _sqrt
    v2_norm = v1_lev / _sqrt
    
    #unwrap phase
    wrap_phase = np.arctan2(v2_norm, v1_norm)
    delta_wrap_phase = wrap_phase - phase_offset
    if delta_wrap_phase > pidiff:
        pc -= 1
    elif delta_wrap_phase < -pidiff:
        pc += 1
    phase_offset = wrap_phase
    phase = wrap_phase + (2*np.pi * pc)
    
    #convert phase to position
    position = phase / (4*np.pi) * 632.8e-9 #[m]
    outfile.write('{0},{1},{2},{3:.4f},{4:.4f}\n'.format(time, v1, v2, phase, position))