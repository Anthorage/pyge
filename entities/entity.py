from sfml.graphics import Drawable, Sprite
import math


class Entity(Drawable):

    def __init__(self, texture, rect):
        super().__init__()

        self._sprite = Sprite(texture, rect)
        self._group = None

        self.visible = True
        self.dead = False

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        if value != None:
            value.add(self)

    def _set_group(self, val):
        self._group = val

    def collides(self, entity):
        return self.global_bounds.intersects(entity)

    def draw(self, target, states):
        target.draw(self._sprite, states)

    def update(self, dt):
        pass

    def move(self, vec):
        self._sprite.move(vec)

    @property
    def position(self):
        return self._sprite.position

    @position.setter
    def position(self, value):
        self.move(value - self._sprite.position)

    def move_towards(self, target, speed):
        pos = self._sprite.position
        dif = target-self._sprite.position
        #dx = tx-pos.x
        #dy = ty-pos.y

        angle = math.atan2(dif.y, dif.x)#math.atan2(dy, dx)
        sqdis = dif.x*dif.x+dif.y*dif.y

        reached = sqdis > speed*speed

        if reached:
            self.move( dif )
        else:
            self.move((speed * math.cos(angle), speed * math.sin(angle)))

        return reached
