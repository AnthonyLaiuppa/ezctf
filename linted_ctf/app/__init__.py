from flask import Flask, render_template

def create_app(test_config=None):
    """Initialize Application"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY = ''
            )
    if test_config is None:
        #Load in production instance settings
        #TODO Move into JSON config thats loaded or env vars
        app.config.update({
            'MYSQL_HOST': '',
            'MYSQL_USER': '',
            'MYSQL_PASSWORD': '',
            'MYSQL_DB': 'ezctf',
            'MYSQL_CURSORCLASS': 'DictCursor'
            })

    else:
        #Loadup them test options
        app.config.update(test_config)

	#Load out DB wrapper so we can pass it to the blueprints
    from app.extensions import mysql
    mysql.init_app(app)

	#Import our blueprints
    from app import auth, cruds
    app.register_blueprint(auth.bp)
    app.register_blueprint(cruds.bp)

    app.add_url_rule('/', endpoint='index')

    #404 Error handling has to be done at app level because of blueprints
    @app.errorhandler(404)
    def page_not_found(e):
      return render_template('404.html'), 404

    return app

