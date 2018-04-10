import os
from app import app, db
from app import User


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
