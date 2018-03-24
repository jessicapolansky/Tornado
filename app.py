import tornado.ioloop
import tornado.web
import tornado.log

import os

from jinja2 import \
  Environment, PackageLoader, select_autoescape

ENV = Environment(
  loader=PackageLoader('myapp', 'templates'),
  autoescape=select_autoescape(['html', 'xml'])
)

class TemplateHandler(tornado.web.RequestHandler):
  def render_template (self, tpl, context):
    template = ENV.get_template(tpl)
    self.write(template.render(**context))

class MainHandler(TemplateHandler):
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    name = self.get_query_argument('name', 'Nobody')
    amount = self.get_query_argument('amount', '0')
    amount = float(amount)
    amount = amount * 1.15
    
    context = {
        'name': name,
        'users': ['paul', 'mittens'],
        'amount': amount
    }
    self.render_template("hello.html", context)

class AboutHandler(TemplateHandler):
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template("About.html", {})
    
class BlogHandler(TemplateHandler):
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template("Blog.html", {})
    
def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
    (r"/About.html", AboutHandler),
    (r"/Blog.html", BlogHandler),
    (
      r"/static/(.*)",
      tornado.web.StaticFileHandler,
      {'path': 'static'}
    ),
  ], autoreload=True)
  
if __name__ == "__main__":
  tornado.log.enable_pretty_logging()
  
  app = make_app()
  PORT = int(os.environ.get('PORT', '8000'))
  app.listen(PORT)
  tornado.ioloop.IOLoop.current().start()
  
