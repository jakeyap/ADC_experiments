`timescale 100ns/1ns

module adc_fsm_testbench;
   
   wire fire_comp, comp_done, comp_result, sample, adc_done;
   wire [11:0] dac_value, result;
   reg  [11:0] reference = 0;
   
   reg delayed_comp_done=0;
   reg delayed_comp_result=0;
   reg delayed_fire_comp=0;
   reg st_conv, rst;
   
   reg [12:0] index = 0;
   reg [11:0]  summary_results;
   
   always @(comp_done) delayed_comp_done <= #0.5 comp_done;
   always @(comp_result) delayed_comp_result <= #0.5 comp_result;
   always @(fire_comp) delayed_fire_comp <= #0.5 fire_comp;
   
   adc_fsm_v0 adc1(  .st_conv(st_conv),
                     .clkout(fire_comp),
                     .clkin(delayed_comp_done),
                     .sample(sample),
                     .result(result),
                     .dac_value(dac_value),
                     .comp_in(delayed_comp_result),
                     .adc_done(adc_done),
                     .rst(rst));

   ideal_comparator comp1( .vip(reference), 
                           .vin(dac_value), 
                           .comp_result(comp_result), 
                           .comp_done(comp_done), 
                           .clk(delayed_fire_comp), 
                           .rst(rst));

   always @ (posedge adc_done or rst) begin
      if (rst) 
         summary_results <= 0;
      else
         summary_results <= result;
   end
   
   initial
   begin
      st_conv = 0;
      rst = 0;
      $dumpfile("log.vcd");
		$dumpvars;
      #1 rst = 0;
      #1 rst = 1;
      #1 rst = 0;
      
      for (index=0; index<4096; index = index + 1) begin
         #1 rst = 0;
         #1 rst = 1;
         #1 rst = 0;
         #1 st_conv = 1;
         #1 st_conv = 0;
         #28 reference = reference + 1;
      end
      #10 $finish;
   end

endmodule