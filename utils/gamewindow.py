from sfml import sf
from pyge.utils.scenemaster import SceneMaster


class GameWindow:
    current = None

    def __init__(self, videomode, title):
        self.window = sf.RenderWindow( videomode, title )
        self._running = True
        self._clock = sf.Clock()

        GameWindow.current = self

    def stop_game(self):
        self._running = False

    def add_scene(self, scene):
        SceneMaster.get().add(scene)

    def play_scene(self, scene):
        SceneMaster.get().switch(scene)

    def push_scene(self, scene):
        SceneMaster.get().push(scene)

    def pop_scene(self):
        SceneMaster.get().pop()

    @property
    def current_scene(self):
        return SceneMaster.get().current

    @property
    def running(self):
        return self._running

    def update(self, dt):
        SceneMaster.get().update(dt)

    def events(self, event):
        if event.type == sf.Event.CLOSED:
            self.stop_game()

    def process_events(self):
        for event in self.window.events:
            self.events(event)

            SceneMaster.get().events(event)

    def draw(self):
        self.window.clear()
        self.window.draw(SceneMaster.get())
        self.window.display()

    def loop(self):
        while self._running:
            self.process_events()
            self.update( self._clock.restart().seconds )
            self.draw()
