# -*- coding: utf-8 -*-
import os
import StringIO
import hashlib

try:
    from boto.s3.connection import S3Connection
    from boto.s3.key import Key
except ImportError:
    raise ImproperlyConfigured, "Could not load Boto's S3 bindings."


ACCESS_KEY = ""
SECRET_KEY = ""
BUCKET = ""
FILE_ROOT = ""


def syncS3():
    connection = S3Connection(ACCESS_KEY, SECRET_KEY)
    bucket = connection.get_bucket(BUCKET)
    s3_keys = bucket.list()
    save_keys(s3_keys)

def save_keys(keys):
    for key in keys:
        key_string = str(key.key)
        parent_folder = "\\".join(key_string.split("/")[0:2])
        parent_folder = os.path.join(FILE_ROOT, parent_folder)
        key_path = os.path.join(parent_folder, key_string.split("/")[-1])
        if not os.path.exists(parent_folder):
            os.makedirs(parent_folder)
        if not os.path.exists(key_path):
            save_to = open(key_path, "wb")
            key.get_file(save_to)
            save_to.close()
            print "saved: %s" % key_path
        else:
            # etag holds the md5 for the key, wrapped in quotes
            s3_md5 = key.etag.strip('"')
            local_md5 = hashlib.md5(open(key_path, "rb").read()).hexdigest()
            if s3_md5 == local_md5:
                print "already exists, file the same: %s" % key_path
            else:
                save_to = open(key_path, "wb")
                key.get_file(save_to)
                save_to.close()
                print "file changed, overwrote: %s" % key_path
        

if __name__ == "__main__":
    syncS3()
