from whitenoise import WhiteNoise

from app import server

application = WhiteNoise(app)
application.add_files('static/', prefix='static/')