# -*- coding: utf-8 -*-

from flask_restful import Resource,reqparse
from flask import Flask, json
import operator, os, math
from time import time
from colorama import Fore, Style

parser = reqparse.RequestParser()
parser.add_argument('SST')
parser.add_argument('SD')
parser.add_argument('msg_type')

response_times = []

class NSSelection(Resource):

	def __init__(self):
		self.start_time = 0	
		self.elapsed_time = 0		
		self.info = "Class NSSelection implementing Nnssf_Selection running on process: "+str(os.getpid())
		print(self.info)
		self.path = "/NSSF/Nnssf_Selection/v2/api/NSSelection.py"
		self.app = Flask(__name__, static_folder='static')
	
	def get(self):
		self.start_time = time()
		request_args = parser.parse_args()
		print("[NSSF][INFO] --> path "+self.path)

		# Process the req_network_slice_information that comes from AMF
		if operator.eq(request_args['msg_type'],"req_network_slice_information"):
			rep_data = self.req_network_slice_information(request_args)
			response = self.app.response_class(response=json.dumps(rep_data),
                                  status=200,
                                  mimetype='application/json')			
			self.elapsed_time = time() - self.start_time
			print(f"{Fore.GREEN}--> ************************* [NSSF request] [req_network_slice_information] {Style.RESET_ALL}")	
			print(f"{Fore.GREEN}--> ************************* [NSSF request] [elapsed time]: "+ str(self.elapsed_time) +f"{Style.RESET_ALL}")	
			response_times.append(self.elapsed_time)
			#print("response times: ",response_times)	
			#print(len(response_times))		
			if len(response_times)==100:
				print(f"{Fore.RED}--> ************************* [NSSF request] [Average Response Time]: "+ str(sum(response_times)/100.0) +f"{Style.RESET_ALL}")	
		
			return response

		else:
			print("[NSSF][WARNING] --> No msg_type found "+request_args['msg_type'])
			rep_data = {"rep_data":"Msg type not found"}
			response = self.app.response_class(response=json.dumps(rep_data),
                                  status=200,
                                  mimetype='application/json')
			
			return response
	
		
	
	def req_network_slice_information(self, request_args):
		# It is assumed that there is the information of NSSAI
		if operator.eq(request_args['SST'],'4'):
			rep_data = {"rep_data":"AuthorizedNetworkSliceInfo"}
			return rep_data
		else:
			rep_data = {"rep_data":"NoAuthorizedNetworkSliceInfo"}
			return rep_data

	

	