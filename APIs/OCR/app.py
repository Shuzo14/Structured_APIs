from flask import Flask
import routes, logging

UPLOAD_FOLDER = '/tmp/'

app = Flask(__name__)
#app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
logging.basicConfig(filename = '/tmp/record.log', level = logging.DEBUG)

def main():
  # showing different logging levels
  app.logger.debug("debug log info")
  app.logger.info("Info log information")
  app.logger.warning("Warning log info")
  app.logger.error("Error log info")
  app.logger.critical("Critical log info")
  return "testing logging levels."

app.add_url_rule('/ocr/help', methods = ['GET'], view_func = routes.help)
app.add_url_rule('/ocr/aadhar', methods = ['POST'], view_func = routes.aadhar)
app.add_url_rule('/ocr/pan', methods = ['POST'], view_func = routes.pan)
app.add_url_rule('/ocr/dlic', methods = ['POST'], view_func = routes.dlic)

if __name__ == '__main__':
	app.run(debug = True)