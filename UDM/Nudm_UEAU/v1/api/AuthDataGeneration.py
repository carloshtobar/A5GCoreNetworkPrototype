# -*- coding: utf-8 -*-

from flask_restful import Resource,reqparse
from flask import Flask, json
import operator, os, math
from time import time
from colorama import Fore, Style
from sqlalchemy import Column, String, create_engine,LargeBinary
from sqlalchemy.orm import sessionmaker
from .. import tables

parser = reqparse.RequestParser()
parser.add_argument('imsi')
parser.add_argument('msisdn')
parser.add_argument('key')
parser.add_argument('opc')
parser.add_argument('ue_listen_port')
parser.add_argument('msg_type')

response_times = []

class AuthDataGeneration(Resource):

	def __init__(self):	
		self.start_time = 0	
		self.elapsed_time = 0	
		self.info = "Class AuthDataGeneration implementing Nudm_UEAU running on process: "+str(os.getpid())
		print(self.info)
		self.path = "/UDM/Nudm_UEAU/v1/api/AuthDataGeneration.py"
		self.app = Flask(__name__, static_folder='static')
	
	def post(self):
		self.start_time = time()
		request_args = parser.parse_args()
		print("[UDM][INFO] --> path "+self.path)

		# Process the req_ue_authentication_data that comes from AUSF
		if operator.eq(request_args['msg_type'],"req_ue_authentication_data"):
			rep_data = self.req_ue_authentication_data(request_args)
			response = self.app.response_class(response=json.dumps(rep_data),
                                  status=200,
                                  mimetype='application/json')			
			self.elapsed_time = time() - self.start_time
			print(f"{Fore.GREEN}--> ************************* [UDM request] [req_ue_authentication_data] {Style.RESET_ALL}")	
			print(f"{Fore.GREEN}--> ************************* [UDM request] [elapsed time]: "+ str(self.elapsed_time) +f"{Style.RESET_ALL}")	
			response_times.append(self.elapsed_time)
			#print("response times: ",response_times)	
			#print(len(response_times))		
			if len(response_times)==100:
				print(f"{Fore.RED}--> ************************* [UDM request] [Average Response Time]: "+ str(sum(response_times)/100.0) +f"{Style.RESET_ALL}")	
			
			return response

		else:
			print("[UDM][WARNING] --> No msg_type found "+request_args['msg_type'])
			rep_data = {"rep_data":"Msg type not found"}
			response = self.app.response_class(response=json.dumps(rep_data),
                                  status=200,
                                  mimetype='application/json')
			
			return response
	
		
	
	def req_ue_authentication_data(self, request_args):
		# First, ue information is retrieved from bd
		engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/oai_db?charset=utf8')
		DBSession = sessionmaker(bind=engine)
		session = DBSession()
		print("User to search: ",request_args['imsi'])
		users = session.query(tables.Users).filter(tables.Users.imsi==request_args['imsi']).one()
		print('users--> ',users)
		rep_data = {'imsi':users.imsi,'msisdn':users.msisdn,'key':'8baf473f2f8fd09487cccbd7097c6862','opc':'e734f8734007d6c5ce7a0508809e7e9c'}        
		
		return rep_data
		
		# AUTHENTICATION_FAILURE
		#if operator.eq(request_args['SST'],'4'):
		#	rep_data = {"rep_data":"AuthorizedNetworkSliceInfo"}
		#	return rep_data
		#else:
		#	rep_data = {"rep_data":"NoAuthorizedNetworkSliceInfo"}
		#	return rep_data

	

	