module ideal_comparator_10b_signed(  vip, 
                              vin, 
                              comp_result, 
                              comp_done, 
                              clk, 
                              rst);
   
   input [11:0] vip, vin;
   input clk, rst;
   output reg comp_result, comp_done;
   
   always @ (posedge clk) begin
      if (!comp_done) begin
         comp_result <= ($signed(vip) >= $signed(vin));
         comp_done <= 1;
      end
   end
   
   always @ (negedge clk or rst) begin
      comp_result <= 0;
      comp_done <= 0;
   end
   
endmodule