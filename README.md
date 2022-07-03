# ascii-flow-charts
Create ascii flow charts for use in code comments

This python program was developed to help me better comment my code by converting a text input file into formatted flow charts.

## Input file:
```
nodes
a=bootloader
b=init
c=read i2c
d=monitor interupts
e=poll GPIO
f=transmit data

coordinates
a=A2
b=B2
c=C1
d=C2
e=C3
f=D2

vertices
a,b
b,c
b,d
b,e
c,f
d,f
e,f
```
## Output chart:
```
 
                                  |                                   
                          ___________________                         
                         |                   |                        
                         |    bootloader     |                        
                         |                   |                        
                          -------------------                         
                                  |                                   
                                  |                                   
                          ___________________                         
                         |                   |                        
                         |       init        |                        
                         |                   |                        
                          -------------------                         
            ______________________|______________________             
           |                      |                      |            
   ___________________    ___________________    ___________________  
  |                   |  |                   |  |                   | 
  |     read i2c      |  | monitor interupts |  |     poll GPIO     | 
  |                   |  |                   |  |                   | 
   -------------------    -------------------    -------------------  
           |______________________|______________________|            
                                  |                                   
                          ___________________                         
                         |                   |                        
                         |   transmit data   |                        
                         |                   |                        
                          -------------------                         
                                  | 
```                                 
