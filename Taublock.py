# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 11:27:27 2019
Y[n] = a x X[n] + b x Y[n-1]
where 
a = ( sample period ) / ( sample period + time constant)
and
b = 1 - a
refer to wikipedia 
https://en.wikipedia.org/wiki/Low-pass_filter#Discrete-time_realization

@author: YYK
"""
import numpy as np

class Taublock:
   def __init__(self, timestep=1e-6):
      self._tau = 1
      self._oldstate = 0
      self._timestep = timestep
      self._alpha = 0
      self._beta = 0
      self._recalculate_alpha_beta()
   
   def read_output(self):
      return self._oldstate
   
   def update_output(self,newstate):
      '''
      Call this with an input to tell output.
      Argument: input value
      '''
      self._oldstate = self._beta * self._oldstate + self._alpha * newstate
      return self._oldstate
   
   def set_initial_condition(self,ic):
      '''
      Call this to set the initial value of the lpf
      Argument: initial condition value
      '''
      self._oldstate = ic
      
   def _recalculate_alpha_beta(self):
      '''
      This gets called internally to recalculate decay weights
      '''
      self._alpha = self._timestep / (self._timestep + self._tau)
      self._beta = (1 - self._alpha)
   
   def set_tau(self,tau):
      self._tau = tau
      self._recalculate_alpha_beta()
      
   def set_analog_lpf_freq(self, lpf_freq):
      tau = 1 / (2 * np.pi * lpf_freq)
      self.set_tau(tau)
   
   def set_timestep (self, timestep):
      self._timestep = timestep
      self._recalculate_alpha_beta()


if __name__ == '__main__':
   import matplotlib.pyplot as plt
   #plt.cla()
   tau = 1
   timestep = 0.1
   maxtime = 10
   lpf1 = Taublock(timestep)
   lpf1.set_tau(tau)
   
   counter = 0
   timeaxis = []
   output1 = []
   out1 = lpf1.update_output(0)
   
   while (counter < maxtime):
      timeaxis.append(counter)
      output1.append(out1)
      out1 = lpf1.update_output(1)
      counter = counter + timestep
   
   plt.plot(timeaxis, output1, marker = '+', color='blue')
   plt.grid(True)