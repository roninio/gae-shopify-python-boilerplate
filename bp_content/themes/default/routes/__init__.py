"""
Using redirect route instead of simple routes since it supports strict_slash
Simple route: http://webapp-improved.appspot.com/guide/routing.html#simple-routes
RedirectRoute: http://webapp-improved.appspot.com/api/webapp2_extras/routes.html#webapp2_extras.routes.RedirectRoute
"""
from webapp2_extras.routes import RedirectRoute
from bp_content.themes.recomend.handlers import handlers

secure_scheme = 'https'

# Here go your routes, you can overwrite boilerplate routes (bp_includes/routes)

_routes = [
    RedirectRoute('/secure/', handlers.SecureRequestHandler, name='secure', strict_slash=True),
    RedirectRoute('/shop', handlers.Shop, name='shopoverview', strict_slash=True),
    RedirectRoute('/shop/<provider_name>/products', handlers.Products, name='shopproducts', strict_slash=True),
    RedirectRoute('/shop/<provider_name>/assets', handlers.Assets, name='shopAssets', strict_slash=True),
	RedirectRoute('/shop/finalize', handlers.Shopifyfinaliaze, name='finalize', strict_slash=True),
	RedirectRoute('/shop/<provider_name>/gettoken', handlers.Shopifystart, name='finalize', strict_slash=True),

]

def get_routes():
    return _routes

def add_routes(app):
    if app.debug:
        secure_scheme = 'http'
    for r in _routes:
        app.router.add(r)
