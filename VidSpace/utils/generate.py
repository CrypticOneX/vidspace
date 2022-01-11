import random
import string


def generate_string(length):
    x = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return x


def generate_file_name(filename):
    return filename.rsplit('.', 1)[1].lower()
