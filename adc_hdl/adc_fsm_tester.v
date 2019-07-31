`timescale 100ns/1ns

module adc_fsm_tester (comp_out, comp_done, st_conv, clk, vin);
   output reg clk, comp_out, comp_done, st_conv = 0;
   
   reg start_clocking = 0;
   output reg [11:0] vin = 0;
   reg [12:0] counter = 0;
   reg [11:0] temp = 0;
   reg [3:0] pointer = 11;
   
   // Run the test once
   initial
   begin
      clk = 0;
      // Dump results of simulation to log.vcd
      $dumpfile("log.vcd");
		$dumpvars;
      // Generate the signals to ADC
      
      #400 $finish;
   end
   
   // Generate periodic clk signal if st_conv is fired
   always begin
      if (start_clocking) begin 
         #1 clk <= 1;
         #1 clk <= 0;
         comp_done <= 0;
      end
      else #1 clk <= 0;
   end
   
   always @ (posedge clk) begin
      comp_out <= vin[pointer];
      comp_done <= 1;
      pointer <= pointer - 1;
   end
   
   always begin
      for (counter=0; counter<4096; counter = counter + 1) begin
         #1 st_conv = 1;
         #1 st_conv = 0;
         #1 start_clocking = 1;
         #24 start_clocking = 0;
         #1 vin = vin + 1;
         temp = vin;
         pointer = 11;
      end
   end
endmodule