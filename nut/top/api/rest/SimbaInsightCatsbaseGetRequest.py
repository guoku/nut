'''
Created by auto_sdk on 2013-11-15 12:58:10
'''
from top.api.base import RestApi
class SimbaInsightCatsbaseGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.category_ids = None
		self.filter = None
		self.nick = None
		self.time = None

	def getapiname(self):
		return 'taobao.simba.insight.catsbase.get'
