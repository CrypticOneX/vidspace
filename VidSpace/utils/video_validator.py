ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', '3gp', 'mp3', 'mkv', 'webm'}
ALLOWED_THUMB_EXTENSION = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_thumb_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_THUMB_EXTENSION
