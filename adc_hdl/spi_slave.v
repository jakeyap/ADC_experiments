module spi_slave(clk,miso,mosi,ss);
   input clk;
   input [0:0] mosi;
   input ss;
   
   output reg[0:0] miso;
   
   reg [7:0] address, data;
   
   reg write_bit;
   reg [7:0] arr [0:309];
   reg k;
   reg [6:0] i=0;
   
   initial begin
      arr[233]=185;
   end
   
   always @(mosi or ss)begin
      // On the 1st bit, catch hold of the write bit.
      if(i==0 && ss==0)begin
         write_bit <= mosi;
      end
   end
   
   always @(posedge clk or mosi)begin
      if(ss==0)begin

         //******ADDRESS READ***//
         if(i>0 && i<9) 
            address <= {address[6:0],mosi};

         //******DATA READING****//
         if(i>8 && i<17 && write_bit==1)
            data <= {data,mosi};

         //*********DATA SENDING TO MASTER MISO***//
         else if(i>8 && i<17 && write_bit==0)begin
            miso <= arr[address][7];
            arr[address] <= arr[address]<<1;
         end
         if(i==17)
            miso <= 1'bz;

         //******DATA RECEIVED WRITTEN IN TO THE ADDRESS***//
         i<=i+1;
         if(i>16 && write_bit==1)
            arr[address]<=data;
      end

   end
endmodule