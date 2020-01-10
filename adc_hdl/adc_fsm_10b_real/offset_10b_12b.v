module offset_10b_12b(  vin, 
                        vout,
                        osc);

   input [11:0] vin, osc;
   output [11:0] vout;
   
   reg [11:0] vin_se;
   reg [11:0] osc_se;
   
   always @ * begin
      vin_se <= {2'b0, vin[9:0]};         // zero extend the inputs
      osc_se <= {{2{osc[9]}},osc[9:0]};   // sign extend the offset      
   end
   
   assign vout = vin_se + osc_se;
   
endmodule