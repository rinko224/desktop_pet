from bestdori.characters import Character
from core.config import config



class Character(Character):
    def __init__(self, character_id : int):
        super().__init__(character_id)

    def get_costume_list(self):
        result = [k for k, v in config.costume_config.items() if v.get("characterId") == self.id]
        return result