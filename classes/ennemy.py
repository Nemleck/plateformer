import pyglet
from pyglet import gl
from pyglet.window import key
from . import functions

from .gameobject import GameObject

# load images
images = {
    "blob": pyglet.image.load("sources/ennemies/blob.png")
}

class Ennemy(GameObject):
    def __init__(self, pos, enn_type: str):
        if enn_type in images.keys():
            self.image = images[enn_type]
            self.sprite = pyglet.sprite.Sprite(self.image)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

            self.size: list[int] = [5, 5]

            self.sprite.scale_x = self.size[0]
            self.sprite.scale_y = self.size[1]
        else:
            return
        
        # place the Ennemy
        self.pos: list[int] = pos

        # some move and animation property
        self.can_move = True
        self.speed_mod: int|float = 1
        self.animation: str|None = None

        self.type = enn_type

        self.update([0,0])
    
    def update(self, scrolling):
        self.sprite.x = self.pos[0] - scrolling[0]
        self.sprite.y = self.pos[1] - scrolling[1]
        
        return self.sprite