module conditional_offset( vin, 
                           vout,
                           offset);

   input [9:0] vin, offset;
   output [9:0] vout;
   
   reg [9:0] vout;
   reg [9:0] flipped_offset;
   
   always @ (*) begin
      flipped_offset = ~offset + 10'd1;
      
      if (offset[9]) begin // if negative number
         if (vin > flipped_offset)
            vout = vin - flipped_offset;
         else
            vout = 10'd0;  // set a floor at 0
      end
      else begin           // if positive number
         if (vin < (10'd 1023 - offset))
            vout = vin + offset;
         else
            vout = 10'd1023;
      end
   end
endmodule