from flask_uploads import UploadSet, IMAGES
from core.choices import PROFILE_PIC_PATH

PROFILE_PIC_SET = UploadSet('profilePics', IMAGES, default_dest=lambda x: PROFILE_PIC_PATH)