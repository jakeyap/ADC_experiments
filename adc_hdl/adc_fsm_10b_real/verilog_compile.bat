REM this is a comment
REM compile the offset cancellation sim
iverilog -o file_osc testbench_adc_fsm_osc.v adc_fsm_10b_v1.v offset_10b_12b.v ideal_comparator_10b_signed.v samplehold.v

REM compile the 12 step scheme sim
iverilog -o file_red testbench_adc_fsm_12s.v adc_fsm_10b_v1.v conditional_offset.v ideal_comparator_10b.v samplehold.v 

REM run the binary files
vvp file_osc
vvp file_red

REM to get "press any key to continue"
pause