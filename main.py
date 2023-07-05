import pyglet
from classes.player import *
from classes.functions import *
from classes.gameobject import *

# Create a window and a moveable surface
win_width = 800
win_height = 600
window = pyglet.window.Window(win_width, win_height, "game")

# Create a player
player = Player()

# Create gameobject list
gameobjects = []
hook1 = GameObject("hook", 39, 72, 900, 350)
hook2 = GameObject("hook", 39, 72, 400, 300)
gameobjects.append(hook1)
gameobjects.append(hook2)

# labels init

coords_label = pyglet.text.Label('[0,0]',
    font_name='Impact',
    font_size=15,
    x=window.width//2, y=window.height-15,
    anchor_x='center', anchor_y='top')

coords_label.color = (0,0,0,255)

rewind_labed = pyglet.text.Label('0',
    font_name='Impact',
    font_size=30,
    x=15, y=window.height-15,
    anchor_x='left', anchor_y='top')

rewind_labed.color = (0,0,0,255)

# Create plateform
plateform1 = GameObject("grass", 1090, 1550, 0, -1550)
plateform3 = GameObject("grass", 1090, 1550, 890, -1350)
plateform4 = GameObject("grass", 1090, 1550, -890, -1350)
plateform2 = GameObject("rock", 412, 92, 340, 125, special_ability=50)
gameobjects.append(plateform1)
gameobjects.append(plateform2)
gameobjects.append(plateform3)
gameobjects.append(plateform4)

# sort all gamobjects based on y
result = []
for gameobject in gameobjects:
    found = False
    for i in range(len(result)):
        if result[i].pos[1] < gameobject.pos[1]:
            result.insert(i, gameobject)
            found = True
            break
    
    if not found:
        result.append(gameobject)

gameobjects = [elm for elm in result] # create copy of the sorted list

# Setup background
bg_img = pyglet.image.load("sources/plateform/background.png")
bg_sprite = pyglet.sprite.Sprite(bg_img, 0, 0)
bg_sprite.scale_x = win_width
bg_sprite.scale_y = win_height

clouds_img = pyglet.image.load("sources/plateform/clouds.png")
clouds_sprite = pyglet.sprite.Sprite(clouds_img, 0, 0)
clouds_sprite.scale = 2
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

# Var init
scrolling = [0, 0]
bg_x_scrolling = 0
foundGround = False

# Setup Keyboard
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

def render_update(dt):
    global scrolling, bg_x_scrolling

    bg_x_scrolling += 5*dt

    window.clear()

    # draw the background
    bg_sprite.draw()

    clouds_sprite.x = -500 - scrolling[0] + bg_x_scrolling
    clouds_sprite.y = -500 - scrolling[1]
    clouds_sprite.draw()
    
    # draw every objects
    for gameobject in gameobjects:
        if gameobject.is_visible(win_width, win_height, scrolling):
            sprite = gameobject.sprite
            gameobject.update(dt)

            if type(sprite) is pyglet.sprite.Sprite:
                sprite.x = gameobject.pos[0] - scrolling[0]
                sprite.y = gameobject.pos[1] - scrolling[1]
                sprite.draw()

    # draw the player
    for player_sprite in player.update(scrolling):
        player_sprite.draw()
    
    # draw UI
    coords_label.draw()

    if player.animation == "rewind":
        rewind_labed.draw()

def game_update(dt):
    global foundGround

    if player.can_move:
        player.move(dt, keys)
    
    elif player.animation == "hook" and not keys[key.Z]:
        if player.tongueOn:
            # make the animation of tongue removing
            player.tongueSize[1] -= 500*dt
            player.pos[1] += 500*dt

            if player.tongueSize[1] <= 50:
                player.tongueOn = False
                player.can_move = True
                player.animation = None

                return
        else:
            # fix flying bugs
            player.animation = None
    
    foundGround = False
    for gameobject in gameobjects:
        if not gameobject:
            continue

        if gameobject.type == "hook":
            # collision with hook ?
            if player.checkCollide(gameobject, True) and player.tongueOn:
                # redefine scrolling so that the object is in the center
                scrolling[0] = - win_width//2 + gameobject.mid_pos(0)
                scrolling[1] = ( - win_height//2 + gameobject.mid_pos(1) ) - win_height//10 # make it a bit higher

                # forbide moving
                player.can_move = False

                # Enable animation bool
                player.animation = "hook"
            
        elif gameobject.type in ["grass", "rock"]:
            # collision with plateform ?
            if player.checkGroundCollide(gameobject):
                foundGround = True
                player.speed_mod = 1
                # player.pos[1] += 100*dt

                gameobject.on_collision()

                continue
    
    # not standing on a plateform ?
    if not foundGround and not player.animation:
        if player.tongueOn:
            player.speed_mod = 0.2
            player.pos[1] -= 50*dt
        else:
            player.speed_mod = 0.5
            player.pos[1] -= 200*dt
    
    # out of the screen ?
    if not player.animation or player.animation in ["rewind"]:
        x_mod = 0
        y_mod = 0
        if player.sprite.y <= 100:
            y_mod = -250
        elif player.sprite.y >= win_height - 350:
            y_mod = 250
        if player.sprite.x <= 300:
            x_mod = -250
        elif player.sprite.x >= win_width - 300:
            x_mod = 250
        
        if x_mod:
            scrolling[0] += x_mod*dt
        if y_mod:
            scrolling[1] += y_mod*dt

        # too low ?
        if player.pos[1] < -1000:
            player.pos[1] = 0
    
    # label update
    coords_label.text = str([round(elm) for elm in player.pos])

    if player.animation == "rewind":
        rewind_labed.text = str(len(player.last_pos))

# Schedule the update and draw functions
pyglet.clock.schedule_interval(game_update, 1/120)
pyglet.clock.schedule_interval(render_update, 1/120)

# Start the application
pyglet.app.run()