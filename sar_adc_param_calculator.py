# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 11:01:40 2019

@author: Bruce Banner
"""
from Taublock import Taublock
import matplotlib.pyplot as plt
import numpy as np

def calculate_sampling_cap_size (num_bits = 10, v_fullscale=1, temp=298):
   '''
   Assumes quantization noise from ADC comes entirely from 
   KT/C noise during the sampling process
   ( K x T ) / C  = D^2 / 12
   Where:
      D = V_fullscale / 2^N
      K = 1.38 x 10^-23
      T = absolute temp
   Args: 
      num_bits: ADC resolution
      v_fullscale: voltage full scale of adc
      temp: operating temp of adc
   Returns:
      C: capacitor size in Farads
   '''
   quant_noise = v_fullscale / (2**num_bits)
   quant_noise = (quant_noise**2) / 12
   
   K = 1.3806e-23
   C = K * temp / (quant_noise)
   print(C)
   # Convert to pF
   C_pf = str(round( C * 1e12 , 3))
   print ("Sampling capacitor size is " + C_pf + "pF")
   return C

def calculate_settling_errors(num_bits=10, 
                              tau = 1, 
                              bit_time_step = 1,
                              timestep = 1e-3,
                              steps = None):
   '''
   Calculate worst case DAC settling errors at each step
   '''
   if steps is None:
      steps = []
      for i in range(num_bits):
         steps.append(2**(num_bits-i-1))
   
   print('Steps: ', end ='')
   print(steps)
   
   lpf = Taublock(timestep=timestep)
   lpf.set_tau(tau)
   
   lpf.set_initial_condition(steps[0])
   
   errors_list = []
   error_trans = []
   dac_outputs = []
   lpf_outputs = []
   time_axis = []
   
   newstate = 2*steps[0]
   for each_step in steps:
      newstate = newstate - each_step
      steps_to_count = bit_time_step / timestep
      counter = 0
      while counter < steps_to_count:
         dac_outputs.append(newstate)
         lpf.update_output(newstate)
         trueref = lpf.read_output()
         lpf_outputs.append(trueref)
         error_trans.append(trueref - newstate)
         counter = counter + 1   
      errors_list.append(round(lpf.read_output() - newstate, 2))
   counter = 0
   for each_element in dac_outputs:
      time_axis.append(counter*timestep)
      counter = counter + 1
   
   return {'steps':steps,
           'time_axis': time_axis,
           'dac_outputs':dac_outputs, 
           'lpf_outputs':lpf_outputs,
           'errors_list':errors_list,
           'error_trans':error_trans}

def calculate_1_cycle_settling(tau):
   return np.exp(-1/tau)
   
   
if __name__ == '__main__':
   #calculate_sampling_cap_size(num_bits=10, v_fullscale=1)
   num_bits = 12
   tau = 0.3
   steps = None
   steps = [2048,1011,456,253,144,80,45,26,14,8,4,3,2,1]
   
   temp = calculate_settling_errors(tau=tau, num_bits=num_bits,steps=steps)
   steps = temp['steps']
   time_axis = temp['time_axis']
   dac_outputs = temp['dac_outputs']
   lpf_outputs = temp['lpf_outputs']
   errors_list = temp['errors_list']
   error_trans = temp['error_trans']
   
   plt.subplot(2,1,1)
   plt.plot(time_axis, dac_outputs)
   plt.plot(time_axis, lpf_outputs)
   plt.yscale('log')
   plt.grid(True)
   plt.subplot(2,1,2)
   plt.plot(time_axis, error_trans)
   plt.yscale('log')
   plt.grid(True)
   for eacherror in errors_list:
      print(eacherror)
   #plt.plot(dac_outputs)
   #plt.plot(lpf_outputs)
   ans1 = steps [0]
   ans2 = steps [0]
   for each in steps[1:]:
      ans1 = ans1 - each
      ans2 = ans2 + each
   print (ans1)
   print (ans2)