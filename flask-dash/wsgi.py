from whitenoise import WhiteNoise

from app import app

application = WhiteNoise(server)
application.add_files('static/', prefix='static/')