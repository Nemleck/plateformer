import pyglet
from pyglet import gl
from pyglet.window import key
from . import functions

from .gameobject import GameObject

import os

# load images
playerIdle = pyglet.image.load("sources/player/idle1.png")
playerOpen = pyglet.image.load("sources/player/open1.png")
playerRewind = pyglet.image.load("sources/player/rewind.png")

class Player(GameObject):
    def __init__(self, pos=[0,200], num=0, upKey=key.Z, leftKey=key.Q, rightKey=key.D, rewindKey=key.A):
        idleExpression = f"sources/player/idle{num+1}.png"
        openExpression = f"sources/player/open{num+1}.png"
        if os.path.exists(idleExpression) and os.path.exists(openExpression):
            self.idleImg = pyglet.image.load(idleExpression)
            self.openImg = pyglet.image.load(openExpression)
        else:
            print("nope")
            self.idleImg = playerIdle
            self.openImg = playerOpen

        self.tongueOn: bool = False
        self.tongueImg = pyglet.image.load("sources/player/tongue.png")
        self.tongueSize = [20, 50]
        self.tonguePos = pos

        self.tongueSprite = pyglet.sprite.Sprite(self.tongueImg, 10, 10)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

        self.size: list[int] = [5, 5]
        self.state = self.idleImg
        
        # place the player
        self.pos: list[int] = pos
        self.last_pos: list[list[int]] = [self.pos]
        self.dt = 0

        # set keys
        self.upKey = upKey
        self.leftKey = leftKey
        self.rightKey = rightKey
        self.rewindKey = rewindKey
        
        self.sprite = pyglet.sprite.Sprite(self.state, x=self.pos[0], y=self.pos[1])
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        self.sprite.scale_x = self.size[0]
        self.sprite.scale_y = self.size[1]

        self.label = pyglet.text.Label(f"p{num+1}",
            font_name='Impact',
            font_size=20,
            color=(0,0,0,255),
            x=0, y=0,
            anchor_x='center', anchor_y='center')
        

        # some move and animation property
        self.can_move = True
        self.speed_mod: int|float = 1
        self.animation: str|None = None

        self.scrolling = [elm for elm in self.pos]

        self.num = num

        self.update([0,0])
    
    def update(self, main_scrolling):
        self.sprite.image = self.state
        self.sprite.x = self.pos[0] - main_scrolling[0]
        self.sprite.y = self.pos[1] - main_scrolling[1]
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        
        # update label
        self.label.x = self.sprite.x + self.size[0]*16//2
        self.label.y = self.sprite.y + self.size[1]*16*1.5

        returnList = [self.sprite, self.label]

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

    def game_update(self, dt, gameobjects, keys, win_width, win_height):
        self.move(dt, keys)
        self.rewind_update(dt, keys)
        self.hook_animation(dt, keys)
        self.collisions(dt, gameobjects, win_width, win_height)
        self.screen_collisions(dt, win_width, win_height)
     
    def move(self, dt, keys):
        if not self.animation and self.can_move:
            # move the player
            if keys[self.leftKey]:
                self.pos[0] -= 300*dt * self.speed_mod
            if keys[self.rightKey]:
                self.pos[0] += 300*dt * self.speed_mod
            if keys[self.upKey] and self.speed_mod >= 1:
                if not self.tongueOn:
                    self.state = self.openImg
                    self.tongueOn = True
                
                else:
                    self.tongueSize[1] += 600*dt

                    if self.tongueSize[1] > 400:
                        self.tongueSize[1] = 400
            
            else: # no z key
                self.state = self.idleImg
                self.tongueSize[1] = 50
                self.tongueOn = False

    def rewind_update(self, dt, keys):
        # store positions to rewind
        self.dt += dt
        if self.dt >= 0.2:
            self.dt = 0

            if keys[self.rewindKey] and len(self.last_pos) >= 1:
                self.animation = "rewind"
                self.state = playerRewind
                self.tongueOn = False

                del self.last_pos[0]
            else:
                self.last_pos.insert(0, [round(elm) for elm in self.pos])
                if len(self.last_pos) >= 100:
                    del self.last_pos[-1]
                
                if self.animation == "rewind":
                    self.animation = None
                    self.last_pos = []
        
        elif self.animation == "rewind" and len(self.last_pos) >= 1:
            dt_to_one = 0.2/dt

            x_diff = self.last_pos[0][0] - self.pos[0]
            y_diff = self.last_pos[0][1] - self.pos[1]

            self.pos[0] += x_diff/dt_to_one
            self.pos[1] += y_diff/dt_to_one
    
    def hook_animation(self, dt, keys):
        if self.animation == "hook" and not keys[self.upKey]:
            if self.tongueOn:
                # make the animation of tongue removing
                self.tongueSize[1] -= 500*dt
                self.pos[1] += 500*dt

                if self.tongueSize[1] <= 50:
                    self.tongueOn = False
                    self.can_move = True
                    self.animation = None

                    return
            else:
                # fix flying bugs
                self.animation = None
    
    def collisions(self, dt: int, gameobjects: list[GameObject|None], win_width, win_height):
        foundGround = False
        for gameobject in gameobjects:
            if not gameobject or not gameobject.is_visible(win_width, win_height, self.scrolling):
                continue

            if gameobject.type == "hook":
                # collision with hook ?
                if self.checkCollide(gameobject, True) and self.tongueOn and not self.animation:
                    # redefine scrolling so that the object is in the center
                    if self.num == 0:
                        self.scrolling[0] = - win_width//2 + gameobject.mid_pos(0)
                        self.scrolling[1] = ( - win_height//2 + gameobject.mid_pos(1) ) - win_height//10 # make it a bit higher

                    # forbide moving
                    self.can_move = False

                    # Enable animation bool
                    self.animation = "hook"
                
            elif gameobject.type in ["grass", "rock", "moving_plateform"]:
                # collision with plateform ?
                coll_result = self.checkGroundCollide(gameobject)
                if coll_result[0]:
                    foundGround = True
                    self.speed_mod = 1

                    if coll_result[1]:
                        gameobject.on_collision()

                    continue
        
        # not standing on a plateform ?
        if not foundGround and not self.animation:
            if self.tongueOn:
                self.speed_mod = 0.2
                self.pos[1] -= 50*dt
            else:
                self.speed_mod = 0.5
                self.pos[1] -= 200*dt
        
        # too low ?
        if self.pos[1] < -1000:
            self.pos[1] = 200
    
    def screen_collisions(self, dt, win_width, win_height):
        # out of the screen ?
        if not self.animation or self.animation in ["rewind"]:
            x_pos = self.pos[0]
            y_pos = self.pos[1]

# p2 = [200, 0]            
# pour que p2 == [0, 0]
# scrolling = [200, 0]
# screen x limits = + -> 300 + 200; - -> <= 300 + 200
# 
# 

            x_mod = 0
            y_mod = 0
            if y_pos <= 100 + self.scrolling[1]:
                y_mod = -250
            elif y_pos >= win_height - 350 + self.scrolling[1]:
                y_mod = 250
            if x_pos <= 300 + self.scrolling[0]:
                x_mod = -250
            elif x_pos >= win_width - 300 + self.scrolling[0]:
                x_mod = 250
            
            if x_mod:
                self.scrolling[0] += x_mod*dt
            if y_mod:
                self.scrolling[1] += y_mod*dt