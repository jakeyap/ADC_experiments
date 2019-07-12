# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 11:34:50 2019
A library for evaluating an ADC ramp file
@author: yap yong keong
"""

#def plot_inls_dnls(directory, filename):
import matplotlib.pyplot as plt
import numpy as np
import csv

def _extract_ramp_from_lists(inputlist, outputlist):
   '''
   This function takes in the in/out lists of an ADC, then does what it needs to return
   a dictionary
   {buckets: histogram horz axis list
   counts: histogram vert axis list
   inl: list of inls
   dnl: list of dnls}
   '''
   largest_output = max(outputlist)
   
   num_bits = int(np.ceil(np.log2(largest_output)))
   print('Number of bits is '+str(round(num_bits,3)))
   buckets = []
   counts = []
   
   for i in range(2**num_bits):
      buckets.append(i)
      counts.append(0)
      
   for each in outputlist:
      counts[each] = counts[each] + 1
   
   cache = _calculate_dnl_inl_histogram(buckets, counts)
   inl = cache['inl']
   dnl = cache['dnl']
   
   return {'inputs': inputlist,
           'outputs': outputlist,
           'buckets': buckets,
           'counts': counts,
           'inl': inl,
           'dnl': dnl,
           }

def _extract_lists_from_file(directory, filename, ignore_row=0, ignore_col=0):
   '''
   This function extracts the transfer function of an ADC from a csv file.   
   Function returns a list of lists
   [inputlist, outputlist]
   '''
   rawfile = open(directory+filename, 'r')
   file = csv.reader(rawfile)
    
   inputs = []
   outputs = []
   counter = 0
   for eachrow in file:
      if (counter > ignore_row):
         inputs.append( float(eachrow[ignore_col+0]) )
         outputs.append( int(eachrow[ignore_col+1]) )
      counter = counter + 1
    
   return [inputs, outputs]

def _plot_histogram(buckets, counts, name='histogram'):
   '''
   This function plots the histogram of an ADC.
   buckets: all the codes available
   counts: frequency of code
   '''
   # need to set the range well
   average_count = sum(counts[1:-1])
   average_count = average_count / (len(counts)-2)
   print('Average count is '+str(round(average_count,3)))
   plt.title(name)
   plt.plot(buckets, counts)
   plt.ylabel('Counts')
   plt.ylim([0,average_count * 2])
   plt.xlabel('Codes')
   plt.grid(True)

def _plot_ramp(inputs, outputs, name='ramp'):
   '''
   This function plots the transfer function of an ADC.
   inputs: input DAC codes
   outputs: ADC output
   '''
   plt.title(name)
   plt.plot(inputs,outputs)
   plt.ylabel('Outputs')
   plt.xlabel('Inputs')
   plt.grid(True)

def _calculate_dnl_inl_histogram(buckets, counts):
   '''
   This function calculates the DNL
   returns a dictionary 
   {'inl': inl, 'dnl': dnl}
   '''
   # calculate average step size
   avg_counts = sum(counts[1:-1]) # exclude lowest & highest codes
   avg_counts = avg_counts / (len(counts)-2) # exclude highest & lowest codes
   
   dnl = []
   for each_count in counts:
      dnl_figure = (each_count - avg_counts) / avg_counts
      dnl.append(dnl_figure)
   
   inl = [0]
   inl_figure = 0
   # exclude for both end points
   for each_dnl in dnl[1:-1]:
      inl_figure = inl_figure + each_dnl
      inl.append(inl_figure)
   inl.append(0)
   
   return {'inl': inl, 'dnl': dnl}

def _plot_inl(buckets, inl, name='INL'):
   '''
   Function name says it all.
   Args: buckets: list of codes
   dnl: dnls of each code
   returns nothing
   '''
   
   temp_buckets = buckets[1:-1]
   temp_inl = inl[1:-1]
   plt.title(name)
   plt.plot(temp_buckets, temp_inl)
   plt.ylim([-4,4])
   plt.ylabel('LSB')
   plt.xlabel('Codes')
   plt.grid(True)

def _plot_dnl(buckets, dnl, name='DNL'):
   '''
   Function name says it all.
   Args: buckets: list of codes
   dnl: dnls of each code
   returns nothing
   '''
   temp_buckets = buckets[1:-1]
   temp_dnl = dnl[1:-1]
   plt.title(name)
   plt.plot(temp_buckets, temp_dnl)
   plt.ylim([-1,1])
   plt.ylabel('LSB')
   plt.xlabel('Codes')
   plt.grid(True)

def eval_adc_from_arrays(inputarr, outputarr):
   '''
   Evaluates ADC from 2 arrays
   Args: 
      inputarr: depends on how many cols u want to ignore in the csv 
      outputarr: depends on how many rows u want to ignore in the csv 
   Returns dictionary for ADC
   '''
   # convert to list
   return eval_adc_from_lists(inputarr.tolist(), outputarr.tolist())

def eval_adc_from_lists(inputlist, outputlist, title=''):
   '''
   Evaluates ADC from 2 lists
   Args: 
      inputlist: depends on how many cols u want to ignore in the csv 
      outputlist: depends on how many rows u want to ignore in the csv 
      title: what to write on top of the plot
   Returns dictionary for ADC
   '''
   cache = _extract_ramp_from_lists(inputlist, outputlist)
   plt.figure(figsize=(12,9))
   plt.suptitle(title)
   plt.subplot(2,2,1)
   _plot_ramp(cache['inputs'],cache['outputs'])
   plt.subplot(2,2,2)
   _plot_histogram(cache['buckets'], cache['counts'])
   plt.subplot(2,2,3)
   _plot_dnl(cache['buckets'], cache['dnl'])
   plt.subplot(2,2,4)
   _plot_inl(cache['buckets'], cache['inl'])
   plt.show()
   return cache
   
def eval_adc_from_file(directory, filename, ignore_row=0, ignore_col=0):
   '''
   Evaluates ADC from a csv file
   Args: 
      directory: duh
      filename: duh, with csv
      ignore_col: depends on how many cols u want to ignore in the csv 
      ignore_row: depends on how many rows u want to ignore in the csv 
   Returns dictionary for ADC
   '''
   [inputlist, outputlist] = _extract_lists_from_file(directory, filename, ignore_row, ignore_col)
   return eval_adc_from_lists(inputlist,outputlist,title=filename)
   
if __name__ == '__main__':
   directory = 'C:/Users/Bruce Banner/Documents/SG/results/done/'
   filename = 'P02A_44_ADC_readings.csv'
   eval_adc_from_file(directory,filename)