import os
import time
import zipfile
import hashlib
import requests
import shutil
import urllib
from urllib.request import urlopen
from pythonopensubtitles.utils import File
from pythonopensubtitles.opensubtitles import OpenSubtitles

# /mnt/i/Movies/Movies
# RESET CODE print(u"\u001b[0m")


class SubtitleBot():
    def __init__(self):
        self.movie_directory = ""
        self.directory_list = ""
        self.directory_size = 0
        self.exit_program = False
        self.sub_db_header = {"user-agent": "SubDB/1.0 (SubtitleBOX/1.0; https://github.com/mitalletap/subtitle-downloader.git)"}
        self.omdb_key = 'a83f21a7'
        self.header = {"user-agent": "mitalletap"}
        # self.header = {"user-agent": "TemporaryUserAgent"} mitalletap
        self.program_load_image()
        print("/mnt/i/Movies/Movies")
        directory, directory_list, directory_size = self.get_folder_information()
        self.movie_directory = directory
        self.directory_list = directory_list
        self.directory_size = directory_size
        while self.exit_program != True:
            self.menu()

    def program_load_image(self):
        print("""
                                          \ | /
                                         '  _  '
                                        -  |_|  -
                                         ' | | '
                                         _,_|___
                                        |   _ []|
                                        |  (O)  |
                                        |_______|


                               ____     __   __  _ __  __   
                              / __/_ __/ /  / /_(_) /_/ /__ 
                             _\ \/ // / _ \/ __/ / __/ / -_)
                            /___/\_,_/_.__/\__/_/\__/_/\__/ 

                       ___                  __             __       
                      / _ \___ _    _____  / /__  ___ ____/ /__ ____
                     / // / _ \ |/|/ / _ \/ / _ \/ _ `/ _  / -_) __/
                    /____/\___/__,__/_//_/_/\___/\_,_/\_,_/\__/_/   
                                                
                                                
                                

        """)

    def display_menu(self):
        print(u" \u26a1 \u001b[36m 1. Print Directory Details \u001b[0m")
        print(u" \u26a1 \u001b[36m 2. Move all Existing Subtitles \u001b[0m")
        print(u" \u26a1 \u001b[36m 3. Delete all Existing Subtitles \u001b[0m")
        print(u" \u26a1 \u001b[36m 4. Download Subtitles For All Movies \u001b[0m")
        print(u" \u26a1 \u001b[36m 5. Show subtitles that could not be downloaded \u001b[0m")
        print(u"\u001b[0m")

    def menu(self):
        loop = True
        while loop:
            self.display_menu()
            choice = input("Enter a Selection: \n")
            if choice == "1":
                self.print_directory_details()
            elif choice == "2":
                dest_dir = input("Choose a Destination Directory for all Subtitles:  \n")
                self.backup_all_subtitles(self.movie_directory, self.directory_list, dest_dir)
            elif choice == "3":
                self.erase_all_subtitles(self.movie_directory, self.directory_list)
            elif choice == "4":
                self.download_all(self.movie_directory, self.directory_list)
            elif choice == "5":
                self.print_list("need_to_redo.txt")
            else:
                loop = False
                exit()

    def add_to_list(self, name, list_name, message, imdb_id="None"):
        with open("{}.txt".format(list_name), "a") as ntr:
            ntr.write(name + ", " + message + ", " + imdb_id + "\n")
            ntr.close()

    def get_hash(self, name, path):
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
        directory = input("Enter the Directory for all Video Folders: \n")
        directory += '/'
        return directory

    def get_folder_information(self):
        directory = self.get_directory()
        directory_list = os.listdir(directory)
        size = len(directory_list)
        return directory, directory_list, size

    def print_list(self, list_name):
        text_file = open(list_name)
        lines = text_file.readlines()
        for line in lines:
            print(line.rstrip())

    def print_list_of_directories(self, arr):
        for dir in arr:
            print(dir)

    def print_directory_details(self):
        count = 1
        print(30*'=', " Top Level Directory ", 30*'=')
        print(self.movie_directory)
        print(30*'='," Movie List ", 30*'=')
        for movie in self.directory_list:
            print(str(count) + ". " + movie)
            count = count + 1
        print(30*'='," # of Movies ", 30*'=')
        print(self.directory_size)

    def get_subtitle_data_from_imdb(self, full_path, movie_directory, movie_name, ost):
        result = ost.search_movies_on_imdb(movie_name)
        imdb_id = result[0]['id']
        link = "https://rest.opensubtitles.org/search/imdbid-{}/sublanguageid-eng".format(imdb_id)
        print(link)
        r = requests.get(link, headers=self.header)
        print(str(r.status_code) + " " + link)
        data = r.json()
        print(u"\u001b[32m Searching for subtitles for {}".format(movie_name) + "\u001b[0m")
        found_any_subs = self.download_all_subtitle_files(data[:3], movie_name, movie_directory)
        if found_any_subs == True:
            self.add_to_list(movie_name, "done", "IMDb", imdb_id)  
            return True
        else:
            print("\u001b[31m No Subs were found for {} \u001b[0m".format(movie_name))
            return False

    def download_subtitle_for_movie_from_the_sub_db(self, movie_name, movie_directory, movie_extension):
        movie_file = movie_directory + movie_name + movie_extension
        hash = self.get_hash(movie_name, movie_file)
        r = requests.get('http://sandbox.thesubdb.com/?action=download&hash={}&language=en'.format(hash), headers=self.sub_db_header)
        try:
            if r.status_code == 200:
                print(u"\u001b[35m Found Subtitle for {} from SUBBD \u001b[0m".format(movie_name))
                with open(movie_directory+'subtitles.subdb.eng.srt', 'wb') as srt:
                    srt.write(r.content)
            return True
        except Exception:
            print(u"\u001b[33m There was an error downloading subtitles from TSDb \u001b[0m")
            return False

    def download_all(self, directory, arr):
        ost = OpenSubtitles()
        token = ost.login(os.environ['OpenSubUserName'], os.environ['OpenSubPassword'])
        redo = 0
        for dir in arr:
            movie_name = dir
            movie_directory = directory + movie_name + '/'
            directory_contents = os.listdir(movie_directory)
            movie_extension, subtitle_exists = self.search_movie_directory_files(movie_name, directory_contents)
            full_path = movie_directory + movie_name + movie_extension
            first_api_status = self.get_subtitle_data_from_imdb(full_path, movie_directory, movie_name, ost)
            if first_api_status == False:
                second_api_status = self.download_subtitle_for_movie_from_the_sub_db(movie_name, movie_directory, movie_extension)
                if second_api_status == False:
                    self.add_to_list(movie_name, "TSDb", "need_to_redo")
                    redo = redo + 1
                else:
                    self.add_to_list(movie_name, "TSDb", "done")  
            time.sleep(1)

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
            subtitle_id = item['SubLanguageID']
            r = requests.get(link, headers=self.header, allow_redirects=True)
            print(r.headers)
            exit()
            # try:
            zip_response = urlopen(link)
            print(u"\u001b[35m Downloading Subtitles for {} \u001b[0m".format(file_name))
            written_zip = open(dest_dir+"/subtitles.zip", "wb")
            written_zip.write(zip_response.read())
            written_zip.close()  
            unzip = zipfile.ZipFile(dest_dir+"subtitles.zip")
            with zipfile.ZipFile(dest_dir+"subtitles.zip") as unzip:
                for item in unzip.namelist():
                    if item.endswith(".srt"):
                        unzip.extract(item, dest_dir)
                        count = self.rename_subtitle_file(count, item, file_name, dest_dir, subtitle_id)
                unzip.close()   
            # except Exception as e:
            #     print("An error occured while writing to ZIP")
        try:
           os.remove(dest_dir+"/subtitles.zip")
           return True
        except Exception:
           self.add_to_list(file_name, "need_to_redo", "ZIP", imdb_id="None")
           return False
    
    def rename_subtitle_file(self, iteration, item, movie_name, dest_dir, subtitle_id):
        movie_without_year = movie_name[0:len(movie_name) - 7]
        movie_without_year = movie_without_year.replace('-', ' ')
        movie_without_year = movie_without_year.replace('.', ' ')
        clean_item = item.replace('-', ' ')
        clean_item = clean_item.replace('.', ' ')
        if movie_without_year in clean_item:
            postfix = movie_name + " - " + str(iteration) + ".{}.srt".format(subtitle_id)
            os.rename(dest_dir+item, dest_dir+postfix)
            iteration = iteration + 1
        else:
            os.remove(dest_dir+item)
        return iteration

    def backup_all_subtitles(self, directory, arr, dest_dir):
        count = 0
        subtitle_extension_type = ['.srt', '.sub'] 
        for sub_directory in arr:
            movie_name = sub_directory
            movie_directory = directory + movie_name + '/'
            directory_contents = os.listdir(movie_directory)
            for item in directory_contents:
                extension = item[-4:]
                if extension in subtitle_extension_type:
                        print(movie_directory+item)
                        count = count + 1
                        shutil.move(movie_directory+item, dest_dir+item)
        print("Finished! {} subtitles transfered".format(count))

    def erase_all_subtitles(self, directory, arr):
        count = 0
        subtitle_extension_type = ['.srt', '.sub'] 
        for sub_directory in arr:
            movie_name = sub_directory
            movie_directory = directory + movie_name + '/'
            directory_contents = os.listdir(movie_directory)
            for item in directory_contents:
                extension = item[-4:]
                if extension in subtitle_extension_type:
                        os.remove(movie_directory+item)
                        print("Removing {}{}".format(movie_name, extension))
                        count = count + 1
        print("Finished! {} subtitles removed".format(count))
                    
        




# bot = SubtitleBot()


print(os.environ.get("USER"))

# ost = OpenSubtitles()
# token = ost.login(os.environ['OpenSubUserName'], os.environ['OpenSubPassword'])
# print(ost.data)
# ost.data




















































































































































































































































































































































































































































































































































































































































































































































# def get_subtitle_data_from_hash(self, full_path, movie_name):
#     ost = OpenSubtitles()
#     token = ost.login(os.environ['OpenSubUserName'], os.environ['OpenSubPassword'])
#     f = File(full_path)
#     other_hash = f.get_hash()
#     try:
#         hash = self.get_hash(movie_name, full_path)
#     except Exception: 
#         print("ERROR WITH HASH")
#     size = f.size

























# apikey = 'a83f21a7'
# movie = "Ant-Man and the Wasp"
# url = f"https://www.omdbapi.com/?apikey={apikey}&s={movie}"
# r = requests.get(url).json()['Search']
# print(r)
# print(r[0]['imdbID'])







# bot.download_all(directory, directory_list)

# /mnt/i/Movies/Movies

# 10 Cloverfield Lane (2016)
# Ant-Man and the Wasp (2018)

# ost = OpenSubtitles()
# token = ost.login(os.environ['OpenSubUserName'], os.environ['OpenSubPassword'])

# file_name = "Ant-Man and the Wasp (2018)"
# directory = "/mnt/i/Movies/Movies/Ant-Man and the Wasp (2018)/"
# file_path = directory + "Ant-Man and the Wasp (2018).mp4"
# f = File(file_path)
# print(f)
# # hash = f.get_hash()
# hash = bot.get_hash(file_name, file_path)
# print(hash)
# size = f.size
# print(size)

# OST
# data = ost.search_subtitles([{ 'moviehash': hash }]) #'sublanguageclear,  'moviebytesize': size
# print("Length is {}".format(str(len(data))))
# print(data)



# SUBDB
# Development API URL: http://sandbox.thesubdb.com/
# Regular URL: http://api.thesubdb.com/
# r = requests.get('http://sandbox.thesubdb.com/?action=download&hash={}&language=en'.format(hash), headers=bot.header)
# if r.status_code == 200:
#     with open(directory+'subtitles.subdb.eng.srt', 'wb') as srt:
#         srt.write(r.content)





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











# data = ost.search_subtitles([{'moviehash': hash }]) #'sublanguageclear,  'moviebytesize': size
# if len(data) > 0:
#     self.download_all_subtitle_files(data, movie_name, movie_directory)
#     self.add_to_list(movie_name, "done")
# else:
#     self.add_to_list(movie_name, "need_to_redo")
# print("Length of {}".format(movie_name) + " is {}".format(str(len(data))))









































































































# import os
# import zipfile
# import hashlib
# import requests
# from urllib.request import urlopen
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
#         # self.header = {"user-agent": "SubDB/1.0 (SubtitleBOX/1.0; https://github.com/mitalletap/subtitle-downloader.git)"}
#         self.header = {"user-agent": "TemporaryUserAgent"}

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
    
#     def download_subtitle_for_movie(self, movie_name, movie_directory, movie_extension, ost):
#         try:
#             full_path = movie_directory + movie_name + movie_extension
#             f = File(full_path)
#             hash = f.get_hash()
#             print(hash)
#             size = f.size
#             print(size)
#             data = ost.search_subtitles([{'sublanguageid': 'eng', 'moviehash': hash, 'moviebytesize': size}])
#             if len(data) > 0:
#                 for item in data:
#                     print(item.ZipDownloadLink)
#             print("Length of {}".format(movie_name) + " is {}".format(str(len(data))))
#         except:
#             print("Didnt work")
#             self.add_to_redo_list(movie_name)

#     def download_all(self, directory, arr):
#         ost = OpenSubtitles()
#         token = ost.login(os.environ['OpenSubUserName'], os.environ['OpenSubPassword'])
#         for dir in arr:
#             movie_name = dir
#             movie_directory = directory + movie_name + '/'
#             print('=================== {} ==================='.format(movie_name))
#             directory_contents = os.listdir(movie_directory)
#             movie_extension, subtitle_exists = self.search_movie_directory_files(movie_name, directory_contents)
#             self.download_subtitle_for_movie(movie_name, movie_directory, movie_extension, ost)

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

#     def download_all_subtitle_files(self, arr, file_name, dest_dir):
#         count = 0
#         for item in arr:
#             link = item['ZipDownloadLink']
#             r = requests.get(link, allow_redirects=True)
#             zip_response = urlopen(link)
#             written_zip = open(dest_dir+"/subtitles.zip", "wb")
#             written_zip.write(zip_response.read())
#             written_zip.close()            
#             unzip = zipfile.ZipFile(dest_dir+"subtitles.zip")
#             with zipfile.ZipFile(dest_dir+"subtitles.zip") as unzip:
#                 for item in unzip.namelist():
#                     if item.endswith(".srt"):
#                         unzip.extract(item, dest_dir)
#                         count = self.rename_subtitle_file(count, item, file_name, dest_dir)
#             unzip.close()   
#         try:
#             os.remove(dest_dir+"/subtitles.zip")
#         except Exception:
#             print("No Zip Created")
    
#     def rename_subtitle_file(self, iteration, item, movie_name, dest_dir):
#         movie_without_year = movie_name[0:len(movie_name) - 7]
#         movie_without_year = movie_without_year.replace('-', ' ')
#         movie_without_year = movie_without_year.replace('.', ' ')
#         clean_item = item.replace('-', ' ')
#         clean_item = clean_item.replace('.', ' ')
#         print(clean_item)
#         print(movie_without_year in clean_item)
#         if movie_without_year in clean_item:
#             postfix = movie_name + " - " + str(iteration) + ".eng.srt"
#             os.rename(dest_dir+item, dest_dir+postfix)
#             iteration = iteration + 1
#         else:
#             os.remove(dest_dir+item)
#         return iteration





# # ost = OpenSubtitles()
# # token = ost.login(os.environ['OpenSubUserName'], os.environ['OpenSubPassword'])

# # file_name = "10 Cloverfield Lane (2016)"
# # directory = "/mnt/i/Movies/Movies/10 Cloverfield Lane (2016)/"
# # file_path = directory + "10 Cloverfield Lane (2016).mp4"
# # f = File(file_path)
# # print(f)
# # hash = f.get_hash()
# # print(hash)
# # size = f.size
# # print(size)
# # data = ost.search_subtitles([{ 'moviehash': hash }]) #'sublanguageclear
# # print("Length is {}".format(str(len(data))))

# bot = SubtitleBot()
# # bot.download_all_subtitle_files(data, file_name, directory)
# directory, directory_list, directory_size = bot.get_folder_information()
# bot.download_all(directory, directory_list)


# # /mnt/i/Movies/Movies
# # curl -A 'TemporaryUserAgent' https://rest.opensubtitles.org/search/moviebytesize-1058175448/moviehash-bc6bc201c2b1ad5c/



# # episode (number)
# # imdbid (always format it as sprintf("%07d", $imdb) - when using imdb you can add /tags-hdtv for example.
# # moviebytesize (number)
# # moviehash (should be always 16 character, must be together with moviebytesize)
# # query (use url_encode, make sure " " is converted to "%20")
# # season (number)
# # sublanguageid (if ommited, all languages are returned)
# # tag (use url_encode, make sure " " is converted to "%20")




