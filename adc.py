# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 10:42:10 2019

@author: YYK
"""
import numpy as np
from Comparator import Comparator
from adc_state_machine import ADC_state_machine as fsm
from Taublock import Taublock
import adc_ramp_processor as adc_eval
import helper_functions as helper

class ADC:
   def __init__(self, tau=1,num_bits=10):
      
      self._timestep = 1/20 # simulation timestep
      self._clock_ratio = 20 # number of timesteps to toggle clock twice
      self._endtime = self._timestep * self._clock_ratio * (num_bits+2)
      
      self._fsm = fsm(bits=num_bits)
      self._com = Comparator()
      self._lpf = Taublock(timestep=self._timestep)
      self._lpf.set_initial_condition(self._fsm.report_current_code())
      self._lpf.set_tau(tau)
      
      self._timeaxis = []  # initialize simulation time axis
      self._clock = []     # initialize clock list
      self.create_clock()  # fill up the time list with timesteps
      self.create_timeaxis() # fill up the clock list
      
      self._codes = []     # for storing transient codes
      self._filtered_ref = [] # for storing the LPF-ed reference respsonse
      self._done = []      # for plotting done signal
      
      self._soln = 0       # for storing final answer
      self._vin = 1        # default analog input to ADC
   
   def run_1_adc_sample(self,vin):
      self.reset_adc()
      self._vin = vin
      self._fsm.st_conv()
      for each_clock_step in self._clock:
         dac = self._fsm.report_current_code()
         lpf = self._lpf.update_output(dac)
         comp_out = self._com.compare(vin,lpf, each_clock_step)
         
         self._fsm.make_decision(comp_out, each_clock_step)
         current_code = self._fsm.report_current_code()
         self._done.append(self._fsm.adc_done())
         self._filtered_ref.append(lpf)
         self._codes.append(current_code)
      self._soln = self._codes[-1]
   
   def create_timeaxis(self):
      self._timeaxis = []
      counter = 0
      while (counter < self._endtime):
         self._timeaxis.append(counter)
         counter = counter + self._timestep
   
   def create_clock(self):
      self._clock = []
      counter = 0
      for each in self._timeaxis:
         if (counter <= self._clock_ratio // 2):
            self._clock.append(0)
         else:
            self._clock.append(1)
         counter = counter + 1
         if (counter >= self._clock_ratio):
            counter = 0
            
   def reset_adc(self):
      self._timeaxis = []
      self._clock = []
      self.create_timeaxis()
      self.create_clock()
      self._codes = []
      self._filtered_ref = []
      self._done = []
      self._soln = 0
   
   def return_transient_results(self):
      timestep_copy = self._timeaxis.copy()
      clock_copy = self._clock.copy()
      codes_copy = self._codes.copy()
      filtered_ref = self._filtered_ref.copy()
      done_copy = self._done.copy()
         
      return {'time': timestep_copy,
              'clock':clock_copy,
              'codes':codes_copy,
              'ref': filtered_ref,
              'done': done_copy}
   
   def set_fsm_steps(self, steps):
      if steps is None:
         pass
      else:
         self._fsm.set_steps(steps)
   
   def return_output(self):
      return self._soln

if __name__ == '__main__':
   num_bits = 12
   offset = 0.5
   tau = 6
   plot_decision_tree = False
   
   steps = [2048,1011,456,253,144,80,45,26,14,8,4,3,2,1]
   
   datasize = int(10 * 2**num_bits)
   #datasize = 1
   input_axis = np.linspace(0,2**num_bits,datasize)
   output_axis = np.zeros(shape=(datasize,),dtype=int)
   counter = 0
   while counter < datasize:
      adcinstance = ADC(tau=tau,num_bits=num_bits)
      inputvoltage = input_axis[counter] + offset
      adcinstance.run_1_adc_sample(vin= inputvoltage)
      plots = adcinstance.return_transient_results()
      output = int(adcinstance.return_output())
      if (plot_decision_tree):
         print(output)
         helper.plot_transients(plots)
      output_axis[counter] = output
      counter = counter + 1
   
   adc_eval.eval_adc_from_arrays(input_axis, output_axis)