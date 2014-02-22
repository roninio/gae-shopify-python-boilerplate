import shopify
import sys
import models 
import logging
from webapp2 import RequestHandler

class Connection(RequestHandler):

	
	def setConnection(self,shop_name):
		devkey = self.app.config.get('shopify_devloper_key')
		devsecret = self.app.config.get('shopify_devloper_secret')

		shopModel = models.Shop()

		shopifyObj = shopModel.get_by_shopname(shop_name)
		if(shopifyObj == None):
			logging.error("Error saving Email Log in datastore")
			return
		#shop_url = "https://"+ key + ":" + secret + "@" + shopname + ".myshopify.com/admin"
		shopify.Session.setup(api_key=devkey, secret=devsecret)
		session = shopify.Session(shopifyObj.shopname + ".myshopify.com", shopifyObj.token)
		shopify.ShopifyResource.activate_session(session)
		shop = shopify.Shop.current