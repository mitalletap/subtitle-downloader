import os
import hashlib
import requests

def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()


hash = get_hash("/mnt/f/School/Github/plex-metadata/justified.mp4")
print(hash)



header = {"user-agent": "SubDB/1.0 (SubtitleBOX/1.0; https://github.com/sameera-madushan/SubtitleBOX.git)"}
url = 'http://api.thesubdb.com/?action=search&hash={}'.format(hash)
req = requests.get(url, headers=header)
print(req.status_code)