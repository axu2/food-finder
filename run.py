import os
from app import app, db
from app import User
from app.compose import compose_email, getMatches


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User,
    'compose_email': compose_email,
    'getMatches': getMatches}


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
