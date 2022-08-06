from instagrapi import Client
from time import sleep, time

class InstaBot:
    def __init__(self, login, password):
        self.client = Client()
        self.client.login(login, password)
        self.users = {}

    def load_media(self, username):
        user_id = self.users[username]
        medias = self.client.user_medias(user_id)
        result = {}
        for m in medias:
            paths = []
            if m.media_type == 1:
                # Photo
                paths.append(self.client.photo_download(m.pk))
            elif m.media_type == 2 and m.product_type == 'feed':
                # Video
                paths.append(self.client.video_download(m.pk))
            elif m.media_type == 2 and m.product_type == 'igtv':
                # IGTV
                paths.append(self.client.video_download(m.pk))
            elif m.media_type == 2 and m.product_type == 'clips':
                # Reels
                paths.append(self.client.video_download(m.pk))
            elif m.media_type == 8:
                # Album
                for path in self.client.album_download(m.pk):
                    paths.append(path)
            else:
                print('Unknown media type:', m.media_type)
            result[m.pk] = paths
            print(f'http://instagram.com/p/{m.code}/', paths)
        return result

    def load_stories(self, usernames):
        self.add_users(usernames)
        stories = []
        for user in usernames:
            user_id = self.users[user]
            stories.append(self.client.user_stories(user_id))
        return stories
        
    def add_users(self, username_list):
        if type(username_list) != list:
            username_list = [username_list]
        for username in username_list:
            if not username in self.users:
                self.users[username] = self.client.user_id_from_username(username)
        return self.users