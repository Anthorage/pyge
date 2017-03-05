from sfml.graphics import Drawable
from pyge.entities.entity import Entity


class Group( Drawable ):

    def __init__(self):
        super().__init__()
        self._entities = []

    def collides(self, who):
        collided = []

        for ent in self._entities:
            if ent.collides(who) and ent != who:
                collided.append(ent)

        return collided

    def collides_group(self, target_group):
        collided = []

        for ent in self._entities:
            coll_pair = []

            for other in target_group:
                if other.collides(ent) and ent != other:
                    coll_pair.append(other)

            collided.append(coll_pair)

        return collided

    def update(self, dt):
        for ic in range( len(self._entities)-1, -1, -1 ):
            ent = self._entities[ic]

            if not ent.dead:
                ent.update(dt)

            if ent.dead:
                self._entities[ ic ] = self._entities.pop()

    def draw(self, target, states):
        for ent in self._entities:
            if ent.visible:
                target.draw(ent, states)

    def add(self, who):
        if isinstance(who, Entity) and who.group != self:
            if who.group != None:
                who._entities.remove(who)
            
            who._set_group(self)
            self._entities.append(who)

    def rem(self, who):
        if who.group == self:
            self._entities.remove(who)