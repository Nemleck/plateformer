import pyglet
from pyglet import gl

images = {
    "hook": pyglet.image.load("./sources/gameobjects/hook.png"),
    "grass": pyglet.image.load("./sources/plateform/grass.png"),
    "rock": pyglet.image.load("./sources/plateform/rock.png")
}

class GameObject:
    def __init__(self, objtype: str, width: int, height: int, x: int, y: int, special_ability: int|None = None):
        self.size = [0, 0]
        self.size[0] = width
        self.size[1] = height

        if objtype in images.keys():
            self.img = images[objtype]
            self.sprite = pyglet.sprite.Sprite(self.img, x, y)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
            
            scaleX = self.size[0]//self.img.width
            scaleY = self.size[1]//self.img.height

            if scaleX >= 1 and scaleY >= 1:
                self.sprite.scale_x = scaleX
                self.sprite.scale_y = scaleY
            else:
                raise ValueError(f"The object of type \"{objtype}\"'s image was too big.")
        else:
            self.img = None
            self.sprite = None

        self.type = objtype
        self.special_ability = special_ability
        self.falling = False

        # place the object
        self.pos = [x, y]

    def update(self, dt):
        # falling ?
        if self.falling:
            self.pos[1] -= self.special_ability*dt

        if self.sprite:
            return self
        else:
            return None
        
    def checkGroundCollide(self, obj: "GameObject", bottom = False):
        x = round(obj.pos[0])
        y = round(obj.pos[1])

        if not bottom:
            y += round(obj.size[1])
        
        self_x1 = round(self.pos[0])
        self_x2 = round(self_x1 + self.size[0]*16)
        right_x = x + obj.size[0]

        check_x = False
        print(range(self_x1, self_x2+1), range(x,right_x+1))
        for i in range(self_x1, self_x2+1):
            if i in range(x,right_x+1):
                check_x = True
                break

        return round(self.pos[1] - 1) in range(y-5,y) and check_x
    
    def on_collision(self):
        if self.type == "rock":
            self.falling = True
            print("rockcoll")
        
    def is_mid(self, win_width, win_height):
        if self.sprite:
            return self.mid_pos(0) == win_width//2 and self.mid_pos(1) == win_height//2
        return False
    
    def mid_pos(self, i):
        if not self.sprite or not i in [0,1]:
            return None
        elif i == 0:
            return self.pos[0] + self.sprite.width//2
        elif i == 1:
            return self.pos[1] + self.sprite.height//2
    
    def is_visible(self, win_width, win_height, scrolling):
        x = self.pos[0] - scrolling[0]
        y = self.pos[1] - scrolling[1]

        x2 = x + self.size[0]
        y2 = y + self.size[1]
        
        return ( (x >= 0 and x <= win_width) or (x2 >= 0 and x2 <= win_width) or (x <= 0 and x2 >= win_width) ) and \
            ( (y >= 0 and y <= win_height) or (y2 >= 0 and y2 <= win_height) or (y <= 0 and y2 >= win_height) )