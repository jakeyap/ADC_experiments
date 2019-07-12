# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 09:37:11 2019

@author: YYK
"""
import numpy as np

class ADC_state_machine:
   '''
   Class to define a FSM to control a SAR ADC
   If no args are given, FSM is initialized to a 10 bits, 10 steps
   '''
   def __init__(self,bits=10):
      '''
      Initializes the variables to 10 bits, 10 steps
      '''
      self._num_bits     = bits
      self._num_steps    = bits
      self._current_code = 2**(bits-1)
      self._state = 'DONE'
      self._steps = []
      self._step_pointer = 0
      self._past_clock = 0
      self.set_steps()
      
   def set_num_bits(self, number):
      self._num_bits = number
      self._current_code  = 2**(number-1)
   
   def set_num_steps(self,steps,):
      if (steps < self._num_bits):
         print('Attempted to set steps to '+str(steps))
         self.report_adc_stats()
         print('Operation ignored')
      else:
         self._num_steps = steps
   
   def report_adc_stats(self):
      print('num bits:  ' + str(self._num_bits))
      print('num steps: ' + str(self._num_steps))
      print('clk speed: ' + str(self._clockspeed) +'Hz')
   
   def reset_ADC(self):
      self._state = 'DONE'
      self._step_pointer = 0
   
   def report_current_code(self):
      return self._current_code
   
   def set_steps(self, steps=None):
      if steps is None:
         # do normal binary search
         self.set_num_steps(self._num_bits)
         temp_step_list = []
         counter = self._num_bits-1
         while (counter >= 0):
            temp_step_list.append(2**(counter))
            counter = counter - 1
         self._steps = temp_step_list
      else:
         self._steps = steps.copy()
      return
   
   def make_decision(self, comparator_result,current_clk):
      # Only do things on positive clock edge
      if (current_clk==1 and self._past_clock==0 and self.converting()):
         if (self._step_pointer == self._num_steps):
            # final step of conversion, make one last update
            self._state = 'DONE'
            if (comparator_result):
               self._current_code = self._current_code # done
            else:
               # 1 bit too high, subtract the LSB to get the answer
               self._current_code = self._current_code - self._steps[-1]
         else:
            # in any other step of the conversion
            if (comparator_result):
               self._current_code = self._current_code + self._steps[self._step_pointer]
               # print('+' + str(self._steps[self._step_pointer]))
            else:
               self._current_code = self._current_code - self._steps[self._step_pointer]
               #print('-' + str(self._steps[self._step_pointer]))
            #print('currentcode ' + str(self._current_code))
            self._step_pointer = self._step_pointer + 1
      # Not edge? Just update the clock
      self._past_clock = current_clk
      
   def converting(self):
      return self._state=='SWITCHING'
   
   def st_conv(self):
      self._state = 'SWITCHING'
      self._step_pointer = 0
      self._current_code = self._steps[self._step_pointer]
      self._step_pointer = self._step_pointer + 1
      
   def adc_done(self):
      return self._state == 'DONE'
      