# -*- coding: utf-8 -*-

"""
    A real simple app for using webapp2 with auth and session.

    It just covers the basics. Creating a user, login, logout
    and a decorator for protecting certain handlers.

    Routes are setup in routes.py and added in main.py
"""
# standard library imports

# related third party imports
import httpagentparser

# local application/library specific imports
import bp_includes.models as models_boilerplate
import models
import string
import shopifyconnection
from bp_includes.lib.basehandler import BaseHandler
from bp_includes.lib.decorators import user_required
import shopify
from pprint import pprint
import json
import sys
from models import *

class Shop(BaseHandler):
    @user_required
    def get(self, **kwargs):
        params = {}

        return self.render_template('shop/shop.html', **params)   

class Products(BaseHandler):
    def get(self, provider_name):
        params = {}
        shopifya = shopifyconnection.Connection()
        shopifya.setConnection(provider_name)

        symbolListForSave = []
        products = shopify.Product.find( published_status='published')
        for product in products:
            bb = vars(product)
            if( bb['attributes']['variants'][0].inventory_quantity > 0):
                symbolListForSave.append((bb))
                
        #print symbolListForSave
        params['products2'] = symbolListForSave
        params['products'] = products
        return self.render_template('shop/products.html', **params)    



class Assets(BaseHandler):
    def get(self, provider_name):
        shopifya = shopifyconnection.Connection()
        shopifya.setConnection(provider_name)
        
        assets = shopify.Asset.find()
        # TODO implment this.. 
        #print products



class Shopifyfinaliaze(BaseHandler):
    def get(self):
        
        params = {}
        params['code'] = self.request.get('code')
        params['shop'] = self.request.get('shop')
        params['timestamp'] = self.request.get('timestamp')
        params['signature'] = self.request.get('signature')


        #print params
        
        shopfirst = string.split(params['shop'],'.',1)
        shopfirst = shopfirst[0]
        devkey = self.app.config.get('shopify_devloper_key')
        devsecret = self.app.config.get('shopify_devloper_secret')
        
        shopify.Session.setup(api_key=devkey, secret=devsecret)
        session = shopify.Session( shopfirst + ".myshopify.com")
        token = session.request_token(params)
        
        session = shopify.Session( shopfirst +  ".myshopify.com", token)
        shopify.ShopifyResource.activate_session(session)
        shop = shopify.Shop.current
        
        
        shopModel = models.Shop()
        shopName = shopModel.get_by_shopname(shopfirst)
        if(shopName):
            shopName.token = token
            shopName.put()
            print 'exsits'
        else:
            shopModel.token = token
            shopModel.shopnamelong= params['shop']
            shopModel.shopname =  shopfirst[0]
            shopModel.put()

        self.redirect('/shop/'+shopfirst +'/products')

class Shopifygettoken(BaseHandler):
    def get(self, provider_name):
        shopify.ShopifyResource.clear_session
        devkey = self.app.config.get('shopify_devloper_key')
        devsecret = self.app.config.get('shopify_devloper_secret')
        #shop_url = "https://"+ key + ":" + secret + "@" + shopname + ".myshopify.com/admin"
        shopify.Session.setup(api_key=devkey, secret=devsecret)
        session = shopify.Session(provider_name + ".myshopify.com")
        scope=["write_products","write_themes","read_products","write_script_tags"]
        url = session.create_permission_url(scope)
        self.redirect(url)



class SecureRequestHandler(BaseHandler):
    """
    Only accessible to users that are logged in
    """

    @user_required
    def get(self, **kwargs):
        user_session = self.user
        user_session_object = self.auth.store.get_session(self.request)

        user_info = models_boilerplate.User.get_by_id(long(self.user_id))
        user_info_object = self.auth.store.user_model.get_by_auth_token(
            user_session['user_id'], user_session['token'])

        try:
            params = {
                "user_session": user_session,
                "user_session_object": user_session_object,
                "user_info": user_info,
                "user_info_object": user_info_object,
                "userinfo_logout-url": self.auth_config['logout_url'],
            }
            return self.render_template('secure_zone.html', **params)
        except (AttributeError, KeyError), e:
            return "Secure zone error:" + " %s." % e