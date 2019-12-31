`timescale 100ns/1ns

module testbench_conditional_offset;
   reg [9:0] vin = 0;
   reg [9:0] vout_reg = 0;
   reg [9:0] offset = -10;
   
   reg [10:0] index = 0;
   wire [9:0] vout;
   integer textfile1 = 0;
   
   conditional_offset block1( .vin(vin), 
                              .vout(vout),
                              .offset(offset));
   
   always @ (*) begin
      vout_reg = vout;
   end
   
   
   initial begin
      textfile1 = $fopen("offset_handling.csv","w");
      $fwrite(textfile1,"vin,osc,vout,\n");
      $dumpfile("log_offset_handling.vcd");
		$dumpvars;
      
      for (index=0; index<1024; index = index + 1) begin
         #1 $fwrite(textfile1,"%d,%d,%d\n",vin,offset,vout_reg);
         #1 vin = vin + 1;
      end
      
      #1 $fclose(textfile1);
      #10 $finish;
   end
   
endmodule