# -*- coding: utf-8 -*-

from flask_restful import Resource,reqparse
from flask import Flask, json
import operator, os, requests, math
from time import time
from colorama import Fore, Style

parser = reqparse.RequestParser()
parser.add_argument('imsi')
parser.add_argument('msisdn')
parser.add_argument('key')
parser.add_argument('opc')
parser.add_argument('ue_listen_port')
parser.add_argument('msg_type')

response_times = []
response_times_udm = []

class UEAuthentication(Resource):

	def __init__(self):
		self.start_time = 0	
		self.elapsed_time = 0		
		self.info = "Class UEAuthentication implementing Nausf_Authentication running on process: "+str(os.getpid())
		print(self.info)
		self.path = "/AUSF/Nausf_Authentication/v1/api/UEAuthentication.py"
		self.app = Flask(__name__, static_folder='static')
	
	def post(self):
		self.start_time = time()
		request_args = parser.parse_args()
		print("[AUSF][INFO] --> path "+self.path)

		# Process the req_network_slice_information that comes from AMF
		if operator.eq(request_args['msg_type'],"req_ue_authentication"):
			rep_data = self.req_ue_authentication(request_args)
			response = self.app.response_class(response=json.dumps(rep_data),
                                  status=200,
                                  mimetype='application/json')			
			return response

		else:
			print("[AUSF][WARNING] --> No msg_type found "+request_args['msg_type'])
			rep_data = {"rep_data":"Msg type not found"}
			response = self.app.response_class(response=json.dumps(rep_data),
                                  status=200,
                                  mimetype='application/json')
			
			return response
	
		
	
	def req_ue_authentication(self, request_args):
		# First, ue information is retrieved from udm
		print("[AUSF][INFO] --> Request authentication data from UDM")
		req_ue_authentication_data = "http://127.0.0.1:5031/nudm-ueau/v1/AuthDataGeneration"
		ue_info = {"imsi":request_args['imsi'],'msg_type':'req_ue_authentication_data'}
		self.elapsed_time = time() - self.start_time
		print(f"{Fore.GREEN}--> ************************* [AUSF request] [req_ue_authentication] {Style.RESET_ALL}")	
		print(f"{Fore.GREEN}--> ************************* [AUSF request] [elapsed time]: "+ str(self.elapsed_time) +f"{Style.RESET_ALL}")	
		response_times.append(self.elapsed_time)
		#print("response times: ",response_times)	
		#print(len(response_times))		
		if len(response_times)==100:
			print(f"{Fore.RED}--> ************************* [AUSF request] [Average Response Time]: "+ str(sum(response_times)/100.0) +f"{Style.RESET_ALL}")	
		
		udm_rep_authentication_data = requests.post(req_ue_authentication_data,data=ue_info)
		self.start_time = time()
		print(udm_rep_authentication_data.json())
		print(udm_rep_authentication_data.status_code)
		print()
		# Second, authentication is performed
		if operator.eq(udm_rep_authentication_data.json()['imsi'],request_args['imsi']):
			rep_data = {"rep_data":"AUTHENTICATION_DATA_SUCCESS"}
		else:
			rep_data = {"rep_data":"AUTHENTICATION_FAILURE"}
		
		self.elapsed_time = time() - self.start_time
		print(f"{Fore.GREEN}--> ************************* [AUSF response] [udm_rep_authentication_data] {Style.RESET_ALL}")	
		print(f"{Fore.GREEN}--> ************************* [AUSF response] [elapsed time]: "+ str(self.elapsed_time) +f"{Style.RESET_ALL}")	
		response_times_udm.append(self.elapsed_time)
		#print("response times: ",response_times)	
		#print(len(response_times))		
		if len(response_times_udm)==100:
			print(f"{Fore.RED}--> ************************* [AUSF response] [Average Response Time]: "+ str(sum(response_times_udm)/100.0) +f"{Style.RESET_ALL}")	
			
		return rep_data
		

	

	