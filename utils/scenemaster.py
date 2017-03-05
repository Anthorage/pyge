from sfml.graphics import Drawable

from pyge.utils.scene import Scene


class SceneMaster(Drawable):
    _instance = None

    def __init__(self):
        super().__init__()

        self.current = None
        self.scenes = {}

        self.scene_stack = []

    @classmethod
    def get(cls):
        if cls._instance == None:
            cls._instance = SceneMaster()

        return cls._instance

    def _change(self, goesto):
        comesfrom = self.current

        if self.current:
            self.current.on_exit(goesto)

        self.current = goesto

        if self.current:
            self.current.on_enter(comesfrom)

    def add(self, scene):
        self.scenes[scene.name] = scene

    def push(self, scene, do_events=False):
        tscene = scene if type(scene) is Scene else self.scenes[scene]

        if not scene in self.scene_stack:
            self.scene_stack.append( tscene )

        if do_events == True:
            self._change(tscene)
        else:
            self.current = tscene

    def pop(self):
        stack_q = len(self.scene_stack)

        if stack_q > 0:
            self.scene_stack.pop()

        self.current = self.scene_stack[stack_q-2] if stack_q >= 2 else None

    def switch(self, scene):
        self._change(scene if type(scene) is Scene else self.scenes[scene])

    def update(self, dt):
        if self.current:
            self.current.update(dt)

    def draw(self, target, states):
        if self.current:
            target.draw(self.current, states)

    def events(self, event):
        if self.current:
            self.current.events(event)
