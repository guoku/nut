'''
Created by auto_sdk on 2017.04.19
'''
from top.api.base import RestApi
class TmcAuthGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.group = None

	def getapiname(self):
		return 'taobao.tmc.auth.get'
