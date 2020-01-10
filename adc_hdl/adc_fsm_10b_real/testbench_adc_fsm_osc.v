`timescale 100ns/1ns

module testbench_adc_fsm_osc;
   
   
   reg [11:0] offset = 0;   // Offset to model comparator offset
   
   wire fire_comp1, comp_done1, comp_result1, sample1, adc_done1;
   wire fire_comp2, comp_done2, comp_result2, sample2, adc_done2;
   wire [9:0] dac_value1, result1;
   wire [9:0] dac_value2, result2;
   wire [11:0] float1, float2;
   reg  [11:0] reference = 0;
   integer textfile1 = 0;
   
   reg delayed_comp_done1=0;
   reg delayed_comp_done2=0;
   reg delayed_comp_result1=0;
   reg delayed_comp_result2=0;
   reg delayed_fire_comp1=0;
   reg delayed_fire_comp2=0;
   reg st_conv, rst, cal;
   
   reg [12:0] index = 0;      // Loop counter
   reg [12:0] innerindex = 0; // Inner loop counter
   reg [11:0] summary_results1;
   reg [11:0] summary_results2;
   
   always @(comp_done1) delayed_comp_done1 <= #1 comp_done1;
   always @(comp_done2) delayed_comp_done2 <= #1 comp_done2;
   
   always @(comp_result1) delayed_comp_result1 <= #0.5 comp_result1;
   always @(comp_result2) delayed_comp_result2 <= #0.5 comp_result2;
   
   always @(fire_comp1) delayed_fire_comp1 <= #0.5 fire_comp1;
   always @(fire_comp2) delayed_fire_comp2 <= #0.5 fire_comp2;
   
   samplehold sh1 (  .vin(dac_value1), 
                     .sample(sample1), 
                     .vout(float1));

   samplehold sh2 (  .vin(dac_value2), 
                     .sample(sample2), 
                     .vout(float2));
      
   adc_fsm_10b_v1 adc1( .st_conv(st_conv),
                        .clkout(fire_comp1),
                        .clkin(delayed_comp_done1),
                        .sample(sample1),
                        .result(result1),
                        .dac_value(dac_value1),
                        .dac_msb(),
                        .dac_lsb(),
                        .comp_in(delayed_comp_result1),
                        .adc_done(adc_done1),
                        .rst(rst),
                        .sel_12b(1'b1),
                        .cal(1'b0));
   
   ideal_comparator_10b_signed comp1(  .vip(reference), 
                                       .vin(float1+offset), 
                                       .comp_result(comp_result1), 
                                       .comp_done(comp_done1), 
                                       .clk(delayed_fire_comp1), 
                                       .rst(rst));
   
   adc_fsm_10b_v1 adc2( .st_conv(st_conv),
                        .clkout(fire_comp2),
                        .clkin(delayed_comp_done2),
                        .sample(sample2),
                        .result(result2),
                        .dac_value(dac_value2),
                        .dac_msb(),
                        .dac_lsb(),
                        .comp_in(delayed_comp_result2),
                        .adc_done(adc_done2),
                        .rst(rst),
                        .sel_12b(1'b1),
                        .cal(cal));
                           
   ideal_comparator_10b_signed comp2(  .vip(reference), 
                                       .vin(float2+offset), 
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
         summary_results2 <= 0;
      else
         summary_results2 <= result2;
   end
   
   initial begin
      st_conv = 0;
      rst = 0;
      cal = 0;
      // -------------------------- change this --------------------------
      offset = 1;
      textfile1 = $fopen("log_osc_p1.csv","w");
      // -----------------------------------------------------------------
      $fwrite(textfile1,"ref,adc1,adc2,\n");
      $dumpfile("log_osc.vcd");
		$dumpvars;
      #1 rst = 0;          // reset LO
      #1 rst = 1;          // reset HI
      #1 rst = 0;          // reset LO
      reference = 512;
      #1 cal = 1;          // cal HI
      #1 st_conv = 1;      // ST_CONV HI
      #1 st_conv = 0;      // ST_CONV LO
      // Record results
      #40 $fwrite(textfile1,"%d,%d,%d\n",reference,summary_results1,summary_results2);
      #1 cal = 0;          // cal LO
      #1 reference = 0;
      for (index=0; index<1024; index = index + 1) begin
         for (innerindex=0;innerindex<1; innerindex = innerindex+1) begin
            #1 st_conv = 1;
            #1 st_conv = 0;
            #40 $fwrite(textfile1,"%d,%d,%d\n",reference,summary_results1,summary_results2);
         end
         reference = reference + 1;
      end
      
      #1 $fclose(textfile1);
      #10 $finish;
   end

endmodule