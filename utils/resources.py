from sfml.graphics import Texture
from sfml.audio import SoundBuffer


def texture_id_to_xy(texture, id, tile_width):
    tiles_texture = texture.width/tile_width
    
    return (id % tiles_texture, id // tiles_texture)

class ResourceManager():
    _instance = None

    def __init__(self):
        self._textures = {}
        self._sound_buffers = {}

    def load_texture(self, name, path):
        self._textures[name] = Texture.from_file(path) if type(path) is str else path

    def get_texture(self, name):
        return self._textures[name]

    def drop_texture(self, name):
        del self._textures[name]

    def load_sound(self, path):
        self._sound_buffers = SoundBuffer.from_file(path) if type(path) is str else path

    def get_sound(self, name):
        return self._sound_buffers[name]

    def drop_sound(self, name):
        del self._sound_buffers[name]

    @classmethod
    def get(cls):
        if cls._instance == None:
            cls._instance = ResourceManager()
        
        return cls._instance