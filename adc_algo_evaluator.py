# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 10:42:10 2019

@author: YYK
"""
import numpy as np
import matplotlib.pyplot as plt
import adc
from adc import ADC
import adc_ramp_processor as adc_eval

def static_tests_sweep(num_bits = 7,
                       offset = 0.5,
                       tau = 6,
                       plot_decision_tree = False
                       ):
   
   datasize = int(10 * 2**num_bits)
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
         adc.plot_transients(plots)
      output_axis[counter] = output
      counter = counter + 1
   
   adc_eval.eval_adc_from_arrays(input_axis, output_axis)
   
def time_domain_probe(num_bits = 7,
                       offset = 0.5,
                       tau = 6,
                       vin=0):
   adcinstance = ADC(tau=tau,num_bits=num_bits)
   inputvoltage = vin + offset
   adcinstance.run_1_adc_sample(vin= inputvoltage)
   plots = adcinstance.return_transient_results()
   adc.plot_transients(plots)
   output = int(adcinstance.return_output())
   print('output is '+str(output))
   
if __name__ == '__main__':
   time_domain_test = True
   num_bits = 4
   offset=0.5
   tau=4.52
   vin=3
   if (time_domain_test):
      time_domain_probe(num_bits=num_bits,
                        offset=offset,
                        tau=tau,
                        vin=vin)
   else:
      static_tests_sweep(num_bits=num_bits,
                       offset=offset,
                       tau=tau,
                       plot_decision_tree=False)