# -*- coding: utf-8 -*-

from flask_restful import Resource,reqparse
from flask import Flask, json
import operator, requests, os, math
from time import time
from colorama import Fore, Style

parser = reqparse.RequestParser()
parser.add_argument('SST')
parser.add_argument('SD')
parser.add_argument('msg_type')

response_times = []
response_times_nssf = []
response_times_ausf = []

class InterfaceeNBSide(Resource):

	def __init__(self):	
		self.start_time = 0	
		self.elapsed_time = 0
		self.info = "Class InterfaceeNBSide implementing Namf_Communication running on process: "+str(os.getpid())
		print(self.info)
		self.path = "/AMF/Namf_Communication/v1/api/eNBAndAMFInterface.py"
		self.app = Flask(__name__, static_folder='static')
	
	def post(self):
		self.start_time = time()
		request_args = parser.parse_args()
		print("[AMF][INFO] --> path "+self.path)

		# Process the ue_req_attach_slice that comes from UE
		if operator.eq(request_args['msg_type'],"ue_req_attach_slice"):
			rep_data = self.ue_req_attach_slice(request_args)
			response = self.app.response_class(response=json.dumps(rep_data),
                                  status=200,
                                  mimetype='application/json')			
			return response
		
		# Default if differente Msg type
		else:
			print("[AMF][WARNING] --> No msg_type found "+request_args['msg_type'])
			rep_data = {"rep_data":"Msg type not found"}
			response = self.app.response_class(response=json.dumps(rep_data),
                                  status=200,
                                  mimetype='application/json')
			
			return response
		
		
	
	def ue_req_attach_slice(self, request_args):
		# Call to NSSF operation
		print("En ue_req_attach_slice AMF ")
		req_network_slice_information = "http://127.0.0.1:5011/nnssf-nsselection/v2/NSSelection"
		slice_info = {'SST':request_args['SST'],'SD':request_args['SD'],"msg_type":"req_network_slice_information"}
		print(req_network_slice_information)
		print(slice_info)
		self.elapsed_time = time() - self.start_time
		print(f"{Fore.GREEN}--> ************************* [AMF request] [ue_req_attach_slice] {Style.RESET_ALL}")	
		print(f"{Fore.GREEN}--> ************************* [AMF request] [elapsed time]: "+ str(self.elapsed_time) +f"{Style.RESET_ALL}")	
		response_times.append(self.elapsed_time)
		#print("response times: ",response_times)	
		#print(len(response_times))		
		if len(response_times)==100:
			print(f"{Fore.RED}--> ************************* [AMF request] [Average Response Time]: "+ str(sum(response_times)/100.0) +f"{Style.RESET_ALL}")	
		nssf_rep_nsselection = requests.get(req_network_slice_information,data=slice_info)
		self.start_time = time()		
		print(nssf_rep_nsselection.json())
		print(nssf_rep_nsselection.status_code)
		
		# Request of the registration procedure
		if operator.eq(nssf_rep_nsselection.json()['rep_data'],"AuthorizedNetworkSliceInfo"):
			print("[AMF][INFO] --> Request of the registration procedure "+nssf_rep_nsselection.json()['rep_data'])
			req_ue_authentication = "http://127.0.0.1:5021/nausf-auth/v1/UEAuthentication"
			ue_info = {"imsi":'208930000000001',"msisdn":"28192","key":"8baf473f2f8fd09487cccbd7097c6862","opc":"e734f8734007d6c5ce7a0508809e7e9c","msg_type":"req_ue_authentication","ue_listen_port":'10.112.223.73:5555'}
			self.elapsed_time = time() - self.start_time
			print(f"{Fore.GREEN}--> ************************* [AMF response] [nssf_rep_nsselection] {Style.RESET_ALL}")	
			print(f"{Fore.GREEN}--> ************************* [AMF response] [elapsed time]: "+ str(self.elapsed_time) +f"{Style.RESET_ALL}")	
			response_times_nssf.append(self.elapsed_time)
			#print("response times: ",response_times)	
			#print(len(response_times))		
			if len(response_times_nssf)==100:
				print(f"{Fore.RED}--> ************************* [AMF response] [Average Response Time]: "+ str(sum(response_times_nssf)/100.0) +f"{Style.RESET_ALL}")	
						
			ausf_rep_authentication = requests.post(req_ue_authentication,data=ue_info)
			self.start_time = time()			
			print(ausf_rep_authentication.json())
			print(ausf_rep_authentication.status_code)
			if operator.eq(ausf_rep_authentication.json()['rep_data'],"AUTHENTICATION_DATA_SUCCESS"):
				rep_data = {"rep_data":"REGISTRATION_SUCCESS"}
			else:
				rep_data = {"rep_data":"REGISTRATION_FAILURE"}

			self.elapsed_time = time() - self.start_time
			print(f"{Fore.GREEN}--> ************************* [AMF response] [ausf_rep_authentication] {Style.RESET_ALL}")	
			print(f"{Fore.GREEN}--> ************************* [AMF response] [elapsed time]: "+ str(self.elapsed_time) +f"{Style.RESET_ALL}")	
			response_times_ausf.append(self.elapsed_time)
			#print("response times: ",response_times)	
			#print(len(response_times))		
			if len(response_times_ausf)==100:
				print(f"{Fore.RED}--> ************************* [AMF response] [Average Response Time]: "+ str(sum(response_times_ausf)/100.0) +f"{Style.RESET_ALL}")	
			

		return rep_data

	

	
    
    
    