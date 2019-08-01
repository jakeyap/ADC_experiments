// Adapted from http://math-crunching.blogspot.com/2015/12/sar-logic-verilog-hdl-code.html
// YYK: converted into sort of asynchronous circuit
// implemented as a state machine

`timescale 100ns/1ns

module adc_fsm_12b_generic_v0(   st_conv,
                                 clkout,
                                 clkin,
                                 sample,
                                 result,
                                 dac_value,
                                 comp_in,
                                 adc_done,
                                 rst,
                                 sel_14b);
   
   input  st_conv;         // st_conv has to move from hi to lo to start a conversion
   output clkout;          // clock output to comparator
   input  clkin;           // clock input from comparator
   output sample;          // to S&H switch. Active high
   output [11:0] result;   // final result
   output [11:0] dac_value;// value to feed DAC
   input comp_in;          // comparator output
   output adc_done;        // done=1 when conversion finishes
   input rst;              // for resetting the fsm
   input sel_14b;          // for selecting 12 steps or 14 steps. High means choose 14. Need to reset the ADC to load these values
   
   // reg sample;             // to S&H switch. Active high
   wire clkout;               // clock output to comparator
   // Internal variables and registers
   reg [1:0] state;           // current state in state machine
   reg [11:0] result;         // final ADC answer
   reg [3:0] pointer;         // pointer for the search algo to index the steps
   reg [11:0] steps [13:0];   // array to store step sizes. 12-bit wide steps with depth of 14 steps
   reg [3:0] defaultpointer;  // default pointer to index the ADC steps
   
   // state assignment
   parameter sWait=0, sSample=1, sConv=2, sDone=3;   
   
   // Initialize the step sizes based on T.Ogawa's 2010 paper
   always @ (posedge rst) begin
      if (sel_14b==1) begin
         steps[13] <= 12'd2048;
         steps[12] <= 12'd1011;
         steps[11] <= 12'd456;
         steps[10] <= 12'd253;
         steps[9]  <= 12'd144;
         steps[8]  <= 12'd80;
         steps[7]  <= 12'd45;
         steps[6]  <= 12'd26;
         steps[5]  <= 12'd14;
         steps[4]  <= 12'd8;
         steps[3]  <= 12'd4;
         steps[2]  <= 12'd3;
         steps[1]  <= 12'd2;
         steps[0]  <= 12'd1;
         defaultpointer <= 4'd13;
      end
      else begin
         steps[13]<= 12'd2048;
         steps[12]<= 12'd2048;
         steps[11]<= 12'd2048;
         steps[10]<= 12'd1024;
         steps[9] <= 12'd512;
         steps[8] <= 12'd256;
         steps[7] <= 12'd128;
         steps[6] <= 12'd64;
         steps[5] <= 12'd32;
         steps[4] <= 12'd16;
         steps[3] <= 12'd8;
         steps[2] <= 12'd4;
         steps[1] <= 12'd2;
         steps[0] <= 12'd1;
         defaultpointer <= 4'd11;
      end
      state    <= sWait;
      result   <= 0;
   end
   
   always @ (posedge st_conv) begin
      // If st_conv goes high, start the sampling switch
      state    <= sSample;
      pointer  <= defaultpointer;
      result   <= 0;
   end
   
   always @ (negedge st_conv) begin
      // If st_conv has a falling edge, start the conversion
      state    <= sConv;
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
            end
            else begin
               state    <= sConv;
               pointer  <= pointer - 1;
            end
         end
      sDone : state     <= sWait;
      default : state   <= sWait;
   endcase
   end
   
   assign clkout = (!clkin & (state==sConv));
   assign sample = (state==sSample);  // drive sample and hold
   assign dac_value = result + steps[pointer]; // to drive DAC
   assign adc_done = state==sDone;  // indicate when finished

endmodule
