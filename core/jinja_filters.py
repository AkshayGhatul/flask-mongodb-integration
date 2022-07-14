from flask import current_app
from base64 import b64encode

@current_app.template_filter('b64d')
def b64d(binary_data):
    if binary_data:
        return b64encode(binary_data).decode()
    return None