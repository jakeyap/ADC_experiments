// Adapted from http://math-crunching.blogspot.com/2015/12/sar-logic-verilog-hdl-code.html
// YYK: converted into sort of asynchronous circuit
// implemented as a state machine
// 30th december 2019

`timescale 100ns/1ns

module adc_fsm_10b_v1(  st_conv,
                        clkout,
                        clkin,
                        sample,
                        result,
                        dac_value,
                        dac_msb,
                        dac_lsb,
                        comp_in,
                        adc_done,
                        rst,
                        sel_12b,
                        cal);
                        
   input  st_conv;         // positive edge starts sampling, negative edge starts conversion
   output clkout;          // clock output to comparator
   input  clkin;           // clock input from comparator
   output sample;          // to S&H switch. Active high
   output [9:0] result;    // final result
   output [9:0] dac_value; // value to feed DAC
   output [9:5] dac_msb;   // value for DAC MSB array
   output [4:0] dac_lsb;   // value for DAC LSB array
   input comp_in;          // comparator result
   output adc_done;        // done=1 when conversion finishes
   input rst;              // for resetting the fsm
   input sel_12b;          // for selecting 12 steps or 10 steps. High means choose 12.
   input cal;              // for calibrating out ADC comparator offset
   
   reg [9:0] offset;          // For storing comparator offset
   wire clkout;               // clock output to comparator
   // Internal variables and registers
   reg [1:0] state;           // current state in state machine
   reg [9:0] result;         // final ADC answer
   reg [3:0] pointer;         // pointer for the search algo to index the steps
   reg [9:0] steps [11:0];   // array to store step sizes. 10-bit wide steps with depth of 12 steps
   reg [3:0] defaultpointer;  // default pointer to index the ADC steps
   
   // state assignment
   parameter sWait=0, sSample=1, sConv=2, sDone=3;   
   
   // Initialize the step sizes based on T.Ogawa's 2010 paper
   always @ (posedge rst) begin
      if (sel_12b==1) begin
         steps[11] <= 10'd512;
         steps[10] <= 10'd246;
         steps[9]  <= 10'd113;
         steps[8]  <= 10'd65;
         steps[7]  <= 10'd37;
         steps[6]  <= 10'd21;
         steps[5]  <= 10'd13;
         steps[4]  <= 10'd7;
         steps[3]  <= 10'd4;
         steps[2]  <= 10'd2;
         steps[1]  <= 10'd2;
         steps[0]  <= 10'd1;
         defaultpointer <= 4'd11;
      end
      else begin
         steps[11]<= 10'd512;
         steps[10]<= 10'd512;
         steps[9] <= 10'd512;
         steps[8] <= 10'd256;
         steps[7] <= 10'd128;
         steps[6] <= 10'd64;
         steps[5] <= 10'd32;
         steps[4] <= 10'd16;
         steps[3] <= 10'd8;
         steps[2] <= 10'd4;
         steps[1] <= 10'd2;
         steps[0] <= 10'd1;
         defaultpointer <= 4'd9;
      end
      state    <= sWait;
      result   <= 0;
      offset   <= 10'd0;
      pointer  <= 0;
   end
   
   always @ (posedge st_conv) begin
      // If st_conv goes high, start the sampling switch
      state    <= sSample;
      pointer  <= defaultpointer;
      if (cal)
         result   <= 10'b0;
      else
         result   <= 10'b0 - offset;
   end
   
   always @ (negedge st_conv) begin
      // If st_conv has a falling edge, start the conversion
      state    <= sConv;
      result   <= 10'b0;
   end
   
   // synchronous design
   always @(posedge clkin) begin
   case (state) // choose next state in state machine
      sConv :
         begin
            // clkout <= 0;
            if (comp_in) 
               result <= result + steps[pointer];
            
            // finished once LSB has been done
            if (pointer==0)  begin
               state    <= sDone;
               pointer  <= pointer;
               if (cal) begin
                  //offset <= (result + (steps[pointer] && comp_in)) - 10'd512 ;
                  offset <= 10'd512 - (result + (steps[pointer] && comp_in));
               end
            end
            else begin
               state    <= sConv;
               pointer  <= pointer - 1;
            end
         end
      sDone :   state   <= sWait;
      default : state   <= sWait;
   endcase
   end
   
   assign clkout = (!clkin & (state==sConv));
   assign sample = (state==sSample);  // drive sample and hold
   assign dac_value = result + steps[pointer]; // to drive DAC
   assign dac_lsb[4:0] = dac_value[4:0];
   assign dac_msb[9:5] = 5'd31 - dac_value[9:5];
   assign adc_done = state==sDone;  // indicate when finished

endmodule
