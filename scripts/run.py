"""Start the local educational server with an ephemeral signing key."""
import os
import secrets
from secure_api import create_app

if __name__ == '__main__':
    os.environ.setdefault('JWT_SECRET', secrets.token_hex(32))
    create_app().run(host='127.0.0.1', port=8080, debug=False)
