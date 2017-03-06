from sfml import sf
import os

import json

class Tile:

    def __init__(self, x, y, id):
        self.x = x
        self.y = y

        self.id = id
        self.user_data = 0


class Layer(sf.Drawable):

    def __init__(self, name, texture, layer_width, layer_height, tile_width, tile_height, properties):
        super().__init__()
        self.name = name

        self._tiles = [[None for x in range(layer_width)] for y in range(layer_height)]
        self._texture = texture

        self._width = layer_width
        self._height = layer_height

        self._tile_width = tile_width
        self._tile_height = tile_height

        self._tiles_per_row = self._texture.width / self._tile_width

        self._properties = properties

        self._collision = properties.get("collision", False)

        self._varray = sf.VertexArray( sf.PrimitiveType.QUADS, layer_width*layer_height*4 )

    def _set_varray(self, x, y, sx, sy):
        vert_id = (x + y * self._width) * 4

        self._varray[vert_id].position = sf.Vector2(x * self._tile_width, y * self._tile_height)
        self._varray[vert_id + 1].position = sf.Vector2((x + 1) * self._tile_width, y * self._tile_height)
        self._varray[vert_id + 2].position = sf.Vector2((x + 1) * self._tile_width, (y + 1) * self._tile_height)
        self._varray[vert_id + 3].position = sf.Vector2(x * self._tile_width, (y + 1) * self._tile_height)

        self._varray[vert_id].tex_coords = sf.Vector2(sx * self._tile_width, sy * self._tile_height)
        self._varray[vert_id + 1].tex_coords = sf.Vector2((sx + 1) * self._tile_width, sy * self._tile_height)
        self._varray[vert_id + 2].tex_coords = sf.Vector2((sx + 1) * self._tile_width, (sy + 1) * self._tile_height)
        self._varray[vert_id + 3].tex_coords = sf.Vector2(sx * self._tile_width, (sy + 1) * self._tile_height)

    def _rem_varray(self, x, y):
        vert_id = (x + y * self._width) * 4

        self._varray[vert_id].position = sf.Vector2(x * self._tile_width, y * self._tile_height)
        self._varray[vert_id + 1].position = sf.Vector2(x * self._tile_width, y * self._tile_height)
        self._varray[vert_id + 2].position = sf.Vector2(x * self._tile_width, y * self._tile_height)
        self._varray[vert_id + 3].position = sf.Vector2(x * self._tile_width, y * self._tile_height)

    @property
    def collisionable(self):
        return self._collision

    def has_tile(self, x, y):
        return self._tiles[y][x] != None

    def set_tile(self, x, y, tid):
        if type(tid) is int and tid >= 0:
            sx = tid % self._tiles_per_row
            sy = tid // self._tiles_per_row

            self._tiles[y][x] = Tile(x, y, tid)

            self._set_varray(x, y, sx, sy)
        else:
            self._tiles[y][x] = None

            self._rem_varray(x, y)

    def draw(self, target, states):
        states.texture = self._texture
        target.draw(self._varray, states)


class Tilemap(sf.Drawable):

    def __init__(self, name, options):
        super().__init__()

        self._name = name

        self._groups = set()
        self._layers = {}

        if not type(options) is dict:
            raise TypeError("Options parameter must be a dictionary")

    def add_group(self, grp):
        self._groups.add(grp)

    def remove_group(self, grp):
        self._groups.discard(grp)

    @property
    def name(self):
        return self._name

    def update(self, dt):
        if self._loaded:
            for lay in self._layers:
                lay.update(dt)

            for grp in self._groups:
                grp.update(dt)

    def draw(self, target, states):
        if self._loaded:
            for _, layer in self._layers.items():
                target.draw(layer, states)

            for grp in self._groups:
                target.draw(grp, states)


class TiledTilemap(Tilemap):

    def __init__(self, name, path, filename, options):
        super().__init__(name, options)

        self._loaded = False
        self._texture = None
        
        self._path = path
        self._filename = filename

        self._use_create = options.get( "create", False )
        self._use_json = options.get( "json", True )
        self._use_texture = options.get( "texture", None )
        self.scene = options.get( "utils", None )


    def set_tile(self, clayer, x, y, id):
        coll = clayer.collisionable
        collval = 0 if coll else 1

        clayer.set_tile(x, y, id)

        if type(id) is int and id >= 0:
            if self._collisions[y][x] == -1 or coll == True:
                self._collisions[y][x] = collval
        else:
            self._collisions[y][x] = -1

            for _, val in self._layers.items():
                icollval = 0 if val.collisionable else 1
                if val.has_tile(x, y) and (self._collisions[y][x] == -1 or val.collisionable == True):
                    self._collisions[y][x] = icollval


    def _load_tile_layer(self, layer, tilesx, tilesy, tsx, tsy, props):
        clayer = Layer(layer["name"], self._texture, tilesx, tilesy, tsx, tsy, props)
        self._layers[clayer.name] = clayer

        accum = 0

        for val in layer["data"]:
            ival = int(val) - 1

            if ival >= 0:
                x = accum % tilesx
                y = accum // tilesx

                self.set_tile(clayer, x, y, ival)

            accum += 1

    @property
    def texture(self):
        return self._texture

    def create_object(self, layerdata, x, y, w, h, id, data):
        pass


    def _load_object_layer(self, layer, tsx, tsy, props):
        name = layer["name"]

        for val in layer["objects"]:
            self.create_object(layer, val["x"], val["y"], val["width"], val["height"], val.get("gid", 1)-1, val)


    def clear(self):
        self._layers = {}
        self._groups = []

        self._collisions = None


    def load_json(self):
        data = None
        self._loaded = False

        with open(os.path.join(self._path, self._filename)) as data_file:
            data = json.load(data_file)

        if data != None:
            tilesx = data["width"]
            tilesy = data["height"]

            tsx = int(data["tilewidth"])
            tsy = int(data["tileheight"])

            self.tile_size = sf.Vector2(tsx, tsy)

            self._collisions = [[-1 for x in range(tilesx)] for y in range(tilesy)]

            #self.batch = pyglet.graphics.Batch()

            self.borders = sf.Rect((0, 0), (tilesx*self.tile_size.x, tilesy*self.tile_size.y))
            self.tile_borders = sf.Rect((0, 0), (tilesx, tilesy))

            tilesets_arr = data["tilesets"]

            if len(tilesets_arr) <= 0:
                return False

            tileset_data = tilesets_arr[0]
            data_tw = int(tileset_data["tilewidth"])
            data_th = int(tileset_data["tileheight"])

            data_iw = int(tileset_data["imagewidth"])
            data_ih = int(tileset_data["imageheight"])

            data_ttx = data_iw//data_tw
            data_tty = data_ih//data_th

            fixpath = os.path.join(self._path, os.path.normpath(tileset_data["image"]))

            self._texture = sf.Texture.from_file(fixpath) if self._use_texture == None else self._use_texture

            for layer in data["layers"]:
                layerprops = layer.get("properties", {})

                if layer["type"] == "tilelayer":
                    self._load_tile_layer(layer, tilesx, tilesy, tsx, tsy, layerprops)
                elif layer["type"] == "objectgroup":
                    self._load_object_layer(layer, tsx, tsy, layerprops)

        return True


    def load_tmx(self):
        raise NotImplementedError("XML not implemented, use JSON format")


    def after_load(self):
        pass

    def load(self):
        if self._use_json:
            self._loaded = self.load_json()
        else:
            self._loaded = self.load_tmx()

        if self._loaded:
            self.after_load()
