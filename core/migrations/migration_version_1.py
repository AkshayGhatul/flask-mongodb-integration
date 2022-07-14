from .models import Model
from core.user.documents import User

class UserDocument(Model, name='User'):
    operations = [
        User._get_collection().update_many({}, {'$unset': {'usertype': 1}}),
    ]
