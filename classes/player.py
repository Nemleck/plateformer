import pyglet
from pyglet import gl
from pyglet.window import key
from . import functions

from .gameobject import GameObject

# load images
playerIdle = pyglet.image.load("sources/player/idle.png")
playerOpen = pyglet.image.load("sources/player/open.png")

class Player(GameObject):
    def __init__(self):
        self.idleImg = playerIdle
        self.openImg = playerOpen

        self.tongueOn: bool = False
        self.tongueImg = pyglet.image.load("sources/player/tongue.png")
        self.tongueSize = [20, 50]
        self.tonguePos = [0, 0]

        self.tongueSprite = pyglet.sprite.Sprite(self.tongueImg, 10, 10)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

        self.size: list[int] = [5, 5]
        self.state = playerOpen
        
        # place the player
        self.pos: list[int] = [0, 200]
        
        self.sprite = pyglet.sprite.Sprite(self.state, x=self.pos[0], y=self.pos[1])
        self.sprite.scale_x = self.size[0]
        self.sprite.scale_y = self.size[1]

        # some move and animation property
        self.can_move = True
        self.speed_mod: int|float = 1
        self.animation: str|None = None

        self.update([0,0])
    
    def update(self, scrolling):
        self.sprite.image = self.state
        self.sprite.x = self.pos[0] - scrolling[0]
        self.sprite.y = self.pos[1] - scrolling[1]
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

        returnList = [self.sprite]

        if self.tongueOn:
            # calculate tongue coords
            self.tonguePos = [0,0]
            self.tonguePos[0] = self.sprite.x + self.size[0]*16//2
            self.tonguePos[1] = self.sprite.y + self.size[1]*16//2 - 10
            
            # update tongue
            self.tongueSprite.x = self.tonguePos[0]
            self.tongueSprite.y = self.tonguePos[1]

            self.tongueSprite.scale_x = self.tongueSize[0]/self.tongueImg.width
            self.tongueSprite.scale_y = self.tongueSize[1]/self.tongueImg.height

            returnList.append(self.tongueSprite)

            # make the tongue beeing rendered in first
            returnList.reverse()
        
        return returnList

    def checkCollide(self, obj: "GameObject", tongue=False):
        if not obj.sprite:
            return False
        
        tempObjPos = [obj.sprite.x, obj.sprite.y]
        tempObjSize = [obj.size[0], obj.size[1]]

        if tongue:
            # complicated stuff just to make the tongue collision only 5 pixel height at the top

            tempTonguePos = [elm for elm in self.tonguePos]
            tempTongueSize = [elm for elm in self.tongueSize]

            tempTonguePos[1] = tempTonguePos[1] + tempTongueSize[1] - 5
            tempTongueSize[1] = 5

            tempObjSize[1] = 5

            selfList = functions.range_from_object(tempTonguePos, tempTongueSize)
        
        else:
            # check any collision in any position
            selfList = functions.range_from_object([self.sprite.x, self.sprite.y], self.size)

        objList = functions.range_from_object(tempObjPos, tempObjSize)

        # check for number in common for x and y
        check = [False, False]
        for i in range(2):
            for j in range(len(selfList[i])):
                if selfList[i][j] in objList[i]:
                    check[i] = True

        return check[0] and check[1]
     
    def move(self, dt, keys):
        if not self.can_move:
            return

        # move the player
        if keys[key.Q]:
            self.pos[0] -= 300*dt * self.speed_mod
        if keys[key.D]:
            self.pos[0] += 300*dt * self.speed_mod
        if keys[key.Z]:
            if not self.tongueOn:
                self.state = self.openImg
                self.tongueOn = True
            
            else:
                self.tongueSize[1] += 600*dt

                if self.tongueSize[1] > 400:
                    self.tongueSize[1] = 400
        
        else: # no z
            self.state = playerIdle
            self.tongueSize[1] = 50
            self.tongueOn = False