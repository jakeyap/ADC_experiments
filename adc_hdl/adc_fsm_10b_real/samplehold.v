`timescale 100ns/1ns

module samplehold(vin, sample, vout);
   
   input sample;
   input [9:0] vin; 
   output [11:0] vout;
   
   reg [11:0] vin_se;
   reg [11:0] stored_value;
   
   always @ * begin
      vin_se <= {2'b0, vin[9:0]};
   end
   
   always @ (negedge sample) begin
      stored_value <= 12'd512 - vin_se;
   end
   
   always @ (posedge sample) begin
      stored_value <= 12'd0;
   end
   
   assign vout = $signed(vin_se) - $signed(stored_value);
   
endmodule