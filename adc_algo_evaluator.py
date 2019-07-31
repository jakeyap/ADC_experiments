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
import helper_functions as helper

# weird_steps = [4,2,1,1]
weird_steps = [2048,1011,456,253,144,80,45,26,14,8,4,3,2,1]
#weird_steps = [16,7,5,3,2,1]
#weird_steps = None

#weird_steps = [4,2,1]
#weird_steps = [512, 246, 113,65,37,21,13,7,4,2,2,1]
#weird_steps = [8,6,4,3,2,1]


def static_tests_sweep(num_bits = 7,
                       offset = 0.5,
                       tau = 6,
                       plot_decision_tree = False,
                       bucketsize = 20, 
                       steps = None):
   
   datasize = int(bucketsize * 2**num_bits)
   input_axis = np.linspace(0,2**num_bits,datasize)
   output_axis = np.zeros(shape=(datasize,),dtype=int)
   output_axis2= np.zeros(shape=(datasize,),dtype=int)
   counter = 0
   while counter < datasize:
      adcinstance = ADC(tau=tau,num_bits=num_bits)
      adc2 = ADC(tau=tau,num_bits=num_bits)
      #adcinstance.set_fsm_steps(weird_steps)
      adc2.set_fsm_steps(steps)
      inputvoltage = input_axis[counter] + offset
      adcinstance.run_1_adc_sample(vin= inputvoltage)
      adc2.run_1_adc_sample(vin= inputvoltage)
      plots = adcinstance.return_transient_results()
      plots2 = adc2.return_transient_results()
      output = int(adcinstance.return_output())
      output2= int(adc2.return_output())
      if (plot_decision_tree):
         print(output)
         helper.plot_transients(plots,vin=None)
         helper.plot_transients(plots2,vin=None)
      output_axis[counter] = output
      output_axis2[counter] = output2
      counter = counter + 1
   
   adc_eval.eval_adc_from_arrays(input_axis, output_axis)
   adc_eval.eval_adc_from_arrays(input_axis, output_axis2)
   
def time_domain_probe(num_bits = 10,
                       offset = 0.5,
                       tau = 6,
                       vin=0,
                       steps=None):
   adcinstance = ADC(tau=tau,num_bits=num_bits)
   adc2 = ADC(tau=tau,num_bits=num_bits)
   # adcinstance.set_fsm_steps(weird_steps)
   adc2.set_fsm_steps(steps)
   inputvoltage = vin + offset
   adcinstance.run_1_adc_sample(vin= inputvoltage)
   adc2.run_1_adc_sample(vin= inputvoltage)
   plots = adcinstance.return_transient_results()
   helper.plot_transients(plots, inputvoltage)
   
   plots2 = adc2.return_transient_results()
   helper.plot_transients(plots2, inputvoltage)
   
   output = int(adcinstance.return_output())
   output2 = int(adc2.return_output())
   print('output is '+str(output))
   print('adjusted output is '+str(output2))


if __name__ == '__main__':
   time_domain_test = False
   num_bits = 12
   offset=0.5
   tau=0.35
   vin=3.55
   binsize = 10
   steps = [2048,1011,456,253,144,80,45,26,14,8,4,3,2,1]
   
   if (time_domain_test):
      time_domain_probe(num_bits=num_bits,
                        offset=offset,
                        tau=tau,
                        vin=vin,
                        steps=steps)
      plt.subplot(3,1,2)
      #plt.ylim([0,5])
   else:
      static_tests_sweep(num_bits=num_bits,
                       offset=offset,
                       tau=tau,
                       plot_decision_tree=False,
                       bucketsize=binsize,
                       steps=steps)