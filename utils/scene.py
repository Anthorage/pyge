from sfml.graphics import Drawable

class Scene(Drawable):

    def __init__(self, name, game=None):
        super().__init__()

        self._name = name
        self._game = game

    @property
    def game(self):
        return self._game

    @property
    def name(self):
        return self._name

    def update(self, dt):
        pass

    def draw(self, target, states):
        pass

    def events(self, event):
        pass

    def on_enter(self, previous):
        pass

    def on_exit(self, towards):
        pass
