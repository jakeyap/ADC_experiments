# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 10:23:51 2019

@author: YYK
"""
import numpy as np

class Comparator:
   def __init__(self):
      self._offset = 0
      self._noise  = 0 # scales a normal distribution of noise by this
      self._past_state = 1 # remembers past state
      self._hysteresis = False # decides whether to acc for hysteresis
      self._hys_window = 1e-3  # sets hysteresis window
      self._prevclockstep = 0
   
   def compare(self, pos_input, neg_input, clockstep):
      if (self._prevclockstep==0 and clockstep==1):
         offset = self._offset
         noise = np.random.normal(loc=0, scale=self._noise)
         
         adjusted_pos_input = pos_input + noise + offset
         if (self._hysteresis):
            if (self._past_state == 1): 
               adjusted_pos_input = adjusted_pos_input + self._hys_window / 2
            else:
               adjusted_pos_input = adjusted_pos_input - self._hys_window / 2
         
         state = int( adjusted_pos_input > neg_input )
         self._past_state = state
         return state
      else:
         return self._past_state
   
   def set_hys_window(self, hys):
      self._hys_window = hys
      
   def hys_on(self):
      self._hysteresis = True
   
   def hys_off(self):
      self._hysteresis = False
      
   def set_noise_volt(self, noise):
      self._noise = noise