import os
import zipfile
import hashlib
import requests
from urllib.request import urlopen
from pythonopensubtitles.utils import File
from pythonopensubtitles.opensubtitles import OpenSubtitles

# /mnt/i/Movies/Movies
# https://api.opensubtitles.org/xml-rpc\

##### 
# Ant-Man and the Wasp (2018).mp4
# /mnt/i/Movies/Movies/Ant-Man and the Wasp (2018)/
# 2e9256b5ee58ad02990572328d527656


class SubtitleBot():
    def __init__(self):
        self.movie_directory = ""
        # self.header = {"user-agent": "SubDB/1.0 (SubtitleBOX/1.0; https://github.com/mitalletap/subtitle-downloader.git)"}
        self.header = {"user-agent": "TemporaryUserAgent"}

    def add_to_redo_list(self, name):
        with open("need_to_redo.txt", "a") as ntr:
            ntr.write(name + "\n")
            ntr.close()

    def get_hash(self, name, path, file):
        try:
            readsize = 64 * 1024
            with open(path, 'rb') as f:
                size = os.path.getsize(path)
                data = f.read(readsize)
                f.seek(-readsize, os.SEEK_END)
                data += f.read(readsize)
            return hashlib.md5(data).hexdigest()
        except Exception:
            print("Could Not Verify Hash of {}".format(name))

    def get_directory(self):
        directory = input("Enter the Directory for a Video: \n")
        directory += '/'
        return directory

    def get_folder_information(self):
        directory = self.get_directory()
        directory_list = os.listdir(directory)
        size = len(directory_list)
        print(size)
        return directory, directory_list, size

    def print_list_of_directories(self, arr):
        for dir in arr:
            print(dir)
    
    def download_subtitle_for_movie(self, movie_name, movie_directory, movie_extension, ost):
        try:
            full_path = movie_directory + movie_name + movie_extension
            f = File(full_path)
            hash = f.get_hash()
            print(hash)
            size = f.size
            print(size)
            data = ost.search_subtitles([{'sublanguageid': 'eng', 'moviehash': hash, 'moviebytesize': size}])
            if len(data) > 0:
                for item in data:
                    print(item.ZipDownloadLink)
            print("Length of {}".format(movie_name) + " is {}".format(str(len(data))))
        except:
            print("Didnt work")
            self.add_to_redo_list(movie_name)

    def download_all(self, directory, arr):
        ost = OpenSubtitles()
        token = ost.login()
        for dir in arr:
            movie_name = dir
            movie_directory = directory + movie_name + '/'
            print('=================== {} ==================='.format(movie_name))
            directory_contents = os.listdir(movie_directory)
            movie_extension, subtitle_exists = self.search_movie_directory_files(movie_name, directory_contents)
            print("For {}, the extension is {} and it is {}".format(movie_name, movie_extension, subtitle_exists))
            if subtitle_exists == False:
                print(movie_directory)
                self.download_subtitle_for_movie(movie_name, movie_directory, movie_extension, ost)
            else:
                print("{} already has subtitles".format(movie_name))

    def search_movie_directory_files(self, name, arr):
        movie_extension_types = ['.mp4', '.mkv', '.mov', '.avi', '.flv', '.wmv'] 
        movie_extension = ""
        srt_exists = False
        for item in arr:
            extension = item[-4:]
            if extension == '.srt':
                srt_exists = True
            else:
                if extension in movie_extension_types:
                    movie_extension = extension
        return movie_extension, srt_exists

    def download_all_subtitle_files(self, arr, file_name, dest_dir):
        count = 0
        for item in arr:
            link = item['ZipDownloadLink']
            r = requests.get(link, allow_redirects=True)
            zip_response = urlopen(link)
            written_zip = open(dest_dir+"/subtitles.zip", "wb")
            written_zip.write(zip_response.read())
            written_zip.close()            
            unzip = zipfile.ZipFile(dest_dir+"subtitles.zip")
            with zipfile.ZipFile(dest_dir+"subtitles.zip") as unzip:
                for item in unzip.namelist():
                    if item.endswith(".srt"):
                        unzip.extract(item, dest_dir)
                        self.rename_subtitle_file(count, item, file_name, dest_dir)
            unzip.close()
            count = count + 1
    
    def rename_subtitle_file(self, iteration, item, movie_name, dest_dir):
        movie_without_year = movie_name[0:len(movie_name) - 7]
        print(movie_without_year)
        clean_item = item.replace('-', ' ')
        clean_item = clean_item.replace('.', ' ')
        print(clean_item)
        postfix = movie_name + " - " + str(iteration) + ".srt"
        os.rename(dest_dir+item, dest_dir+postfix)
        # new = movie_name.replace('-', ' ')
        # print(new)

ost = OpenSubtitles()
token = ost.login()

file_name = "Ant-Man and the Wasp (2018)"
directory = "/mnt/i/Movies/Movies/Ant-Man and the Wasp (2018)/"
file_path = directory + "Ant-Man and the Wasp (2018).mp4"
f = File(file_path)
print(f)
hash = f.get_hash()
print(hash)
size = f.size
print(size)
data = ost.search_subtitles([{ 'moviehash': hash }]) #'sublanguageclear
print("Length is {}".format(str(len(data))))

bot = SubtitleBot()
bot.download_all_subtitle_files(data, file_name, directory)

# directory, directory_list, directory_size = bot.get_folder_information()
# bot.download_all(directory, directory_list)


# /mnt/i/Movies/Movies
# curl -A 'TemporaryUserAgent' https://rest.opensubtitles.org/search/moviebytesize-1058175448/moviehash-bc6bc201c2b1ad5c/



# episode (number)
# imdbid (always format it as sprintf("%07d", $imdb) - when using imdb you can add /tags-hdtv for example.
# moviebytesize (number)
# moviehash (should be always 16 character, must be together with moviebytesize)
# query (use url_encode, make sure " " is converted to "%20")
# season (number)
# sublanguageid (if ommited, all languages are returned)
# tag (use url_encode, make sure " " is converted to "%20")














































































































































# import os
# import hashlib
# import requests
# from pythonopensubtitles.utils import File
# from pythonopensubtitles.opensubtitles import OpenSubtitles

# # /mnt/i/Movies/Movies
# # https://api.opensubtitles.org/xml-rpc\

# ##### 
# # Ant-Man and the Wasp (2018).mp4
# # /mnt/i/Movies/Movies/Ant-Man and the Wasp (2018)/
# # 2e9256b5ee58ad02990572328d527656


# class SubtitleBot():
#     def __init__(self):
#         self.movie_directory = ""
#         self.header = {"user-agent": "SubDB/1.0 (SubtitleBOX/1.0; https://github.com/mitalletap/subtitle-downloader.git)"}


#     def login(self):        
#         ost = OpenSubtitles()
#         token = ost.login('droid-53', 'sh!loh10')
#         return token

#     def add_to_redo_list(self, name):
#         with open("need_to_redo.txt", "a") as ntr:
#             ntr.write(name + "\n")
#             ntr.close()

#     def get_hash(self, name, path, file):
#         try:
#             readsize = 64 * 1024
#             with open(path, 'rb') as f:
#                 size = os.path.getsize(path)
#                 data = f.read(readsize)
#                 f.seek(-readsize, os.SEEK_END)
#                 data += f.read(readsize)
#             return hashlib.md5(data).hexdigest()
#         except Exception:
#             print("Could Not Verify Hash of {}".format(name))

#     def get_directory(self):
#         directory = input("Enter the Directory for a Video: \n")
#         directory += '/'
#         return directory

#     def get_folder_information(self):
#         directory = self.get_directory()
#         directory_list = os.listdir(directory)
#         size = len(directory_list)
#         print(size)
#         return directory, directory_list, size

#     def print_list_of_directories(self, arr):
#         for dir in arr:
#             print(dir)
    
#     def download_subtitle_for_movie(self, movie_name, movie_directory, movie_extension):
#         full_path = movie_directory + movie_name + movie_extension
#         hash = self.get_hash(movie_name, full_path)
#         url = 'http://api.thesubdb.com/?action=search&hash={}'.format(hash)
#         req = requests.get(url, headers=self.header)
#         if req.status_code != 200:
#             self.add_to_redo_list(movie_name)
#         print(req.status_code)
#         print(hash)

#     def download_all(self, directory, arr):
#         for dir in arr:
#             movie_name = dir
#             movie_directory = directory + movie_name + '/'
#             print('=================== {} ==================='.format(movie_name))
#             directory_contents = os.listdir(movie_directory)
#             movie_extension, subtitle_exists = self.search_movie_directory_files(movie_name, directory_contents)
#             print("For {}, the extension is {} and it is {}".format(movie_name, movie_extension, subtitle_exists))
#             if subtitle_exists == False:
#                 print(movie_directory)
#                 self.download_subtitle_for_movie(movie_name, movie_directory, movie_extension)
#             else:
#                 print("{} already has subtitles".format(movie_name))

#     def search_movie_directory_files(self, name, arr):
#         movie_extension_types = ['.mp4', '.mkv', '.mov', '.avi', '.flv', '.wmv'] 
#         movie_extension = ""
#         srt_exists = False
#         for item in arr:
#             extension = item[-4:]
#             if extension == '.srt':
#                 srt_exists = True
#             else:
#                 if extension in movie_extension_types:
#                     movie_extension = extension
#         return movie_extension, srt_exists







