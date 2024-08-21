from flask import Flask,render_template



def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object('generative_ai.app.config.config')

    # Register blueprints
    from .main.routes import main  # Import the main blueprint
    from .smart_prompt.routes import smart_prompt
    from .anomaly_guard.routes import anomaly_guard
    from .gen_retrieve.routes import gen_retrieve
    from .local_trainer.routes import local_trainer
    #from .cloud_connect.routes import cloud_connect

    app.register_blueprint(main)
    app.register_blueprint(smart_prompt, url_prefix='/smart_prompt')
    app.register_blueprint(anomaly_guard, url_prefix='/anomaly_guard')
    app.register_blueprint(gen_retrieve, url_prefix='/gen_retrieve')
    app.register_blueprint(local_trainer, url_prefix='/local_trainer')
    #app.register_blueprint(cloud_connect, url_prefix='/cloud_connect')
    
    return app
