# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 15:28:08 2019

@author: yyk
"""

import matplotlib.pyplot as plt

def redundancy_calculator(num_steps=12, num_bits=10):
   redundancy = []
   stepsizes = []
   
   if num_steps < num_bits:
      print('Number of bits = ' + str(num_bits))
      print('Number of steps = ' + str(num_steps))
      print('# Steps must be larger or equal to # bits')
   else:
      pass
      
   return {'redundancy': redundancy, 'stepsizes':stepsizes}

def plot_transients(results, vin=None):
   '''
   Helper function to deal with plotting
   Args: results -> a dictionary containing the following information
   {'time': time axis
   'clock': square wave
   'codes': adc output codes
   'ref': references
   'done': adc done signal}
   '''
   timestep = results['time']
   clock = results['clock']
   codes = results['codes']
   ref = results['ref']
   done = results['done']
   
   plt.figure(1)
   plt.subplot(3,1,1)
   plt.grid(True)
   plt.plot(timestep,clock,color='green')
   plt.ylabel('Clock')
   plt.subplot(3,1,2)
   plt.grid(True)
   plt.plot(timestep,codes, color='gray')
   plt.ylabel('Reference transitions')
   if vin is not None:
      vin_list = []
      for each_element in timestep:
         vin_list.append(vin)
      plt.plot(timestep, vin_list, color='blue')
   
   plt.plot(timestep,ref, color='red')
   plt.subplot(3,1,3)
   plt.grid(True)
   plt.plot(timestep,done,color='purple')
   plt.ylabel('Done')

if __name__ == '__main__':
   output = redundancy_calculator()
   redundancy = output['redundancy']
   stepsizes = output['stepsizes']
   print ('Step sizes\t', '')
   print (stepsizes)
   print ('Redundancy\t', '')
   print (redundancy)