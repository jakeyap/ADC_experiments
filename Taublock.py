# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 11:27:27 2019
Y[n] = b x X[n] + d x Y[n-1]
where 
b + d = 1
d = e(-1/tau)
where tau = 2 x pi x f(normalized to sample freq)
@author: YYK
"""
import numpy as np

class Taublock:
   def __init__(self):
      self._tau = 1
      self._oldstate = 0
      self._decay = 0.001 # weight to hold on to past value
      
   def update_output(self,newstate):
      decay = self._decay
      beta = 1 - decay
      self._oldstate = decay * self._oldstate + beta * newstate
      return self._oldstate
   
   def set_initial_condition(self,ic):
      self._oldstate = ic
      
   def set_tau(self,tau):
      self._tau = tau
      self._decay = np.exp(-1 / tau)
      #print('Tau: '+str(tau))
      #print('Decay factor: ' + str(round(self._decay,3)))