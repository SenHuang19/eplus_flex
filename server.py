import socket
import time as tm
import numpy as np
import sys
import random as rd
import json,collections
import os
import random as rd
from numpy import array
from shutil import copyfile




class socket_server:

    def __init__(self):     
          self.sock=socket.socket()
          self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
          host=socket.gethostname()
          port=5001
          self.sock.bind(("127.0.0.1",port))
          self.sock.listen(10)
		  
def data_parse(data): 
    data=data.replace('[','')     
    data=data.replace(']','')  	
    data=data.split(',')

    for i in range(len(data)):
	              data[i]=float(data[i])
         
    return data

def read_data(file_name): 
    reg=np.loadtxt(file_name)
    reg_ref=[abs(number) for number in reg]
    reg=reg/max(reg_ref)
    return reg

	
def EP(model_path,startmonth,startday,endmonth,endday,timestep):

        f = open(model_path, 'r')
        lines = f.readlines()
        f.close()
		
        for i in range(len(lines)):
            if lines[i].lower().find('runperiod,') != -1:
                lines[i + 2] = '    ' + str(startmonth) + ',                       !- Begin Month' + '\n'
                lines[i + 3] = '    ' + str(startday) + ',                       !- Begin Day of Month' + '\n'
                lines[i + 4] = '    ' + str(endmonth) + ',                      !- End Month' + '\n'
                lines[i + 5] = '    ' + str(endday) + ',                      !- End Day of Month' + '\n'
                lines[i + 6] = '    Monday,                  !- Day of Week for Start Day' + '\n'
            elif lines[i].lower().find('timestep,') != -1 and lines[i].lower().find('update frequency') == -1:
                if lines[i].lower().find(';') != -1:
                    lines[i] = '  Timestep,' + str(timestep) + ';' + '\n'
                else:
                    lines[i + 1] = '  ' + str(timestep) + ';' + '\n'                    
        f = open(model_path, 'w')
        for i in range(len(lines)):
            f.writelines(lines[i])
        f.close()	
	

def write_port_file(port,host):
        fh = open('socket.cfg', "w+")
        fh.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
        fh.write('<BCVTB-client>\n')
        fh.write('  <ipc>\n')
        fh.write('    <socket port="%r" hostname="%s"/>\n' % (port, host))
        fh.write('  </ipc>\n')
        fh.write('</BCVTB-client>')
        fh.close()


	

def writeVariableFile(config):
#    default=[]
    with open(config) as f:
        config=json.load(f,object_pairs_hook=collections.OrderedDict)
        if 'inputs' in config: 
            INPUTS = config['inputs']
#        print INPUTS
        if 'outputs' in config:
            OUTPUTS = config['outputs']
#        print OUTPUTS
        ePlusOutputs=0
        ePlusInputs=0
        fh = open('variables.cfg', "w+")
        fh.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
        fh.write('<!DOCTYPE BCVTB-variables SYSTEM "variables.dtd">\n')
        fh.write('<BCVTB-variables>\n')
        for obj in OUTPUTS.itervalues():
            if obj.has_key('name') and obj.has_key('type'):
                ePlusOutputs = ePlusOutputs + 1
                fh.write('  <variable source="EnergyPlus">\n')
                fh.write('    <EnergyPlus name="%s" type="%s"/>\n' % (obj.get('name'), obj.get('type')))
                fh.write('  </variable>\n')
        for obj in INPUTS.itervalues():
            if obj.has_key('name') and obj.has_key('type'):
                ePlusInputs = ePlusInputs + 1
                fh.write('  <variable source="Ptolemy">\n')
                fh.write('    <EnergyPlus %s="%s"/>\n' % (obj.get('type'), obj.get('name')))
                fh.write('  </variable>\n')
#                default.append(obj.get('default'))
        fh.write('</BCVTB-variables>\n')
        fh.close()
        return ePlusInputs

        

	


server=socket_server()
#EP(sys.argv[1],8,1,8,1,60)
ePlusInputs=writeVariableFile(sys.argv[1])
#print default
write_port_file(5001,'127.0.0.1')

vers = 2
flag = 0

dev=float(sys.argv[2])

dev_act = 100

start=float(sys.argv[3])
          
server.sock.listen(10)

conn,addr=server.sock.accept()
index=1
while 1:


### data received from eplus
         
         data = conn.recv(10240)
		 
         print('I just got a connection from ', addr)
#         print data
         data = data.rstrip()

         arry = data.split() 
#         print arry
         flagt = float(arry[1])
         if flagt==1:
                 conn.close()
                 tm.sleep(1)
                 if not os.path.exists('result'):
                                 os.makedirs('result')
                 copyfile('eplusout.csv', 'result/'+str(start)+'_'+str(dev)+'.csv')
						 
                 sys.exit()
                 
         
         if len(arry)>=6:
#              print arry
             
              time=float(arry[5])
              mssg = '%r %r %r 0 0 %r' % (vers, flag, ePlusInputs, time)              
              for i in range(ePlusInputs):
                          
                          if index>=start*60 and index<start*60+30:                                                   
			                              if dev_act==100:
			                                     if dev<0:
                                                               dev_act = rd.uniform(dev,0)
			                                     else:
                                                               dev_act = rd.uniform(0,dev)                          
                                                  
			                              mssg=mssg+' '+str(dev_act+float(arry[6+i]))
                          elif index<start*60 and index>=start*60-60:                                                                        
			                              mssg=mssg+' '+str(-1*dev+float(arry[6+i]))                          
                          else:
			                              mssg=mssg+' '+str(arry[6+i])						  
              # if index>=start*60 and index<start*60+30:
                           # print mssg
              conn.send(mssg+'\n')
         index=index+1

             

