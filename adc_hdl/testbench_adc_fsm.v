`timescale 100ns/1ns

module adc_fsm_testbench;
   
   wire fire_comp1, comp_done1, comp_result1, sample1, adc_done1;
   wire fire_comp2, comp_done2, comp_result2, sample2, adc_done2;
   wire [11:0] dac_value1, result1;
   wire [11:0] dac_value2, result2;
   reg  [11:0] reference = 0;
   
   reg delayed_comp_done1=0;
   reg delayed_comp_done2=0;
   reg delayed_comp_result1=0;
   reg delayed_comp_result2=0;
   reg delayed_fire_comp1=0;
   reg delayed_fire_comp2=0;
   reg st_conv, rst;
   
   reg [12:0] index = 0;      // loop counter
   reg [12:0] innerindex = 0; // Inner loop counter
   reg [11:0] summary_results1;
   reg [11:0] summary_results2;
   
   integer textfile1 = 0;
   integer textfile2 = 0;
   
   always @(comp_done1) delayed_comp_done1 <= #0.5 comp_done1;
   always @(comp_done2) delayed_comp_done2 <= #0.5 comp_done2;
   
   always @(comp_result1) delayed_comp_result1 <= #0.5 comp_result1;
   always @(comp_result2) delayed_comp_result2 <= #0.5 comp_result2;
   
   always @(fire_comp1) delayed_fire_comp1 <= #0.5 fire_comp1;
   always @(fire_comp2) delayed_fire_comp2 <= #0.5 fire_comp2;
   
   adc_fsm_12b_generic_v0 adc1(.st_conv(st_conv),
                           .clkout(fire_comp1),
                           .clkin(delayed_comp_done1),
                           .sample(sample),
                           .result(result1),
                           .dac_value(dac_value1),
                           .comp_in(delayed_comp_result1),
                           .adc_done(adc_done1),
                           .rst(rst),
                           .sel_14b(1'b0));

   ideal_comparator comp1( .vip(reference), 
                           .vin(dac_value1), 
                           .comp_result(comp_result1), 
                           .comp_done(comp_done1), 
                           .clk(delayed_fire_comp1), 
                           .rst(rst));
   
   adc_fsm_12b_generic_v0 adc2(.st_conv(st_conv),
                           .clkout(fire_comp2),
                           .clkin(delayed_comp_done2),
                           .sample(sample),
                           .result(result2),
                           .dac_value(dac_value2),
                           .comp_in(delayed_comp_result2),
                           .adc_done(adc_done2),
                           .rst(rst),
                           .sel_14b(1'b1));
                           
   ideal_comparator comp2( .vip(reference), 
                           .vin(dac_value2), 
                           .comp_result(comp_result2), 
                           .comp_done(comp_done2), 
                           .clk(delayed_fire_comp2), 
                           .rst(rst));
   
   always @ (posedge adc_done1 or posedge rst) begin
      if (rst) 
         summary_results1 <= 0;
      else
         summary_results1 <= result1;
   end
   
   always @ (posedge adc_done2 or posedge rst) begin
      if (rst) 
         summary_results1 <= 0;
      else
         summary_results2 <= result2;
   end
   
   initial begin
      st_conv = 0;
      rst = 0;
      textfile1 = $fopen("output1.csv","w");
      textfile2 = $fopen("output2.csv","w");
      $dumpfile("log.vcd");
		$dumpvars;
      #1 rst = 0;
      #1 rst = 1;
      #1 rst = 0;
      
      for (index=0; index<4096; index = index + 1) begin
         for (innerindex=0;innerindex<4; innerindex = innerindex+1) begin
            #1 st_conv = 1;
            #1 st_conv = 0;
            #28 $fwrite(textfile1,"%d,%d\n",reference,summary_results1);
            $fwrite(textfile2,"%d,%d\n",reference,summary_results2);
         end
         reference = reference + 1;
      end
      
      #1 $fclose(textfile1);
      #1 $fclose(textfile2);
      #10 $finish;
   end

endmodule