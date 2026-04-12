from typing import Optional
from pathlib import Path
import json

class ConfigManager:
    def __init__(self, config_path : Optional[str] = None):
        if config_path is None:
            config_dir = Path.home() / ".desktop_pet"
            config_dir.mkdir(exist_ok=True)
            config_path = config_dir / "config.json"
        self.config_path = Path(config_path)
        self.costume_config = json.load(open("./resource/config/costume.json", "r", encoding="utf-8"))
        self.user_config = json.load(open("./resource/config/user.json", "r", encoding="utf-8"))

        
config = ConfigManager()