import flaskr
import os

# initialize the db for the first time
if not os.path.isfile("/var/www/flaskr/flaskr/db/flaskr.db"):
      print 'initialing the db...'
      flaskr.init_db()


