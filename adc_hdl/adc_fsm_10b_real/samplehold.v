`timescale 100ns/1ns

module samplehold(vin, sample, topcap, botcap);
   
   input sample;
   input [9:0] vin, botcap; 
   output [9:0] topcap;
   
   reg stored_value;
   
   always @ (negedge sample) begin
      stored_value <= vin - botcap;
   end
   
   assign topcap = botcap + stored_value;
endmodule