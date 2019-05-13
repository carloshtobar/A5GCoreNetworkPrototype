# -*- coding: utf-8 -*-

from threading import Thread
import requests, math
import time as thread_time
from time import time
from colorama import Fore, Style

number_ue = 100
S_NSSAI = {'SST':'4','SD':'Road Authority name'} # Identifies a Network Slice. SST: Slice/Service Type. SD: Slice Diferentiatior
                           # SST=1 (eMBB), 2 (URLLC), 3 (MIoT) Standarized
                           # SST = 4 (Cooperative driving) Not Standarized
                            
response_times = []
start_time = 0	
elapsed_time = 0

def initial_request():
    print("UE initiated")
    ue_req_attach_slice = "http://127.0.0.1:80/namf-comm/v1/amfeNBInterface" 
    slice_info = {'SST':S_NSSAI['SST'],'SD':S_NSSAI['SD'],"msg_type":"ue_req_attach_slice"}
    amf_rep_register = requests.post(ue_req_attach_slice,data=slice_info)
    start_time = time()
    print(amf_rep_register.json())
    print(amf_rep_register.status_code)
    print("UE attachet to the slice")
    elapsed_time = time() - start_time
    print(f"{Fore.GREEN}--> ************************* [UE response] [ue_req_attach_slice] {Style.RESET_ALL}")	
    print(f"{Fore.GREEN}--> ************************* [UE response] [elapsed time]: "+ str(elapsed_time) +f"{Style.RESET_ALL}")	
    response_times.append(elapsed_time)
    #print("response times: ",response_times)	
    #print(len(response_times))		
    if len(response_times)==100:
        print(f"{Fore.RED}--> ************************* [UE response] [Average Response Time]: "+ str(sum(response_times)/100.0) +f"{Style.RESET_ALL}")	
			

for i in range(number_ue):
    t = Thread(target = initial_request,args=())
    t.start()
    t.join()
    thread_time.sleep(0.01)