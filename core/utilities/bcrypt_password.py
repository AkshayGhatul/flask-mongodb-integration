from core import bcrypt

def get_password_hash(password):
    return bcrypt.generate_password_hash(password)