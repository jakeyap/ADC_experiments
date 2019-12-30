module conditional_offset( vin, 
                           vout,
                           offset);

   input [9:0] vin, offset;
   output [9:0] vout;
   
   if 
   vout = vin + offset;
   
endmodule