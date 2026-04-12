import bestdori.costumes as costumes
from core.config import config


class Costume(costumes.Costume):
    def __init__(self, costume_id : int):
        super().__init__(costume_id)

    def get_character(self):
        return config.costume_config[str(self.costume_id)]["characterId"]
               
