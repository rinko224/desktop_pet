import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


from bestdori_ext.Character import Character
from bestdori_ext.Costume import Costume
from PIL import Image
from io import BytesIO
from core.util.picture_deal import picture_spilt
import random
from core.config import config


class LiveSDManager:
    def __init__(self):
        self.livesd: Image = None
        self.character_id: int = None
        self.costume_id: int = None

    def get_live(self):
        return self.livesd

    def gen_live(self, costume_id: int = None):
        costume = Costume(costume_id)
        pic_bytes = costume.get_sdchara()
        picture = picture_spilt(pic_bytes)
        self.livesd = random.choice(picture)
        self.costume_id = costume_id
        # 从costume_id获取character_id
        self.character_id = costume_id // 1000 if costume_id else None

    def random_live(self, character_id : int = None):
        if(character_id is None):
            costume_id = random.randint(26, 2348)
            costume = Costume(costume_id)
            pic_bytes = costume.get_sdchara()
            picture = picture_spilt(pic_bytes)
            self.livesd = random.choice(picture)
            self.costume_id = costume_id
            self.character_id = costume_id // 1000
        else:
            character = Character(character_id)
            costume_list = character.get_costume_list()
            selected_costume_id = random.choice(costume_list)
            costume = Costume(selected_costume_id)
            pic_bytes = costume.get_sdchara()
            picture = picture_spilt(pic_bytes)
            self.livesd = random.choice(picture)
            self.costume_id = selected_costume_id
            self.character_id = character_id

if __name__ == '__main__':
    live_sd_manager = LiveSDManager()
    live_sd_manager.random_live(20)
    live_sd_manager.livesd.show()

   
