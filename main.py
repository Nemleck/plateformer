import pyglet
from classes.player import *
from classes.functions import *
from classes.gameobject import *
from classes.functions import *

# import options
from json import loads
with open("options.json", "r", encoding="utf-8") as f:
    data = loads(f.read())

with open("map.json", "r", encoding="utf-8") as f:
    map = loads(f.read())

# Create a window and a moveable surface
win_width = data["window"]["width"]
win_height = data["window"]["height"]
window = pyglet.window.Window(win_width, win_height, "game")

# Create a player
player = Player(data["player"]["starting_pos"])

# Create gameobject list
gameobjects = []
for json_go_data in map:
    gameobjects.append(
        GameObject(
            json_go_data["type"],
            json_go_data["width"],
            json_go_data["height"],
            json_go_data["x"],
            json_go_data["y"],
            json_go_data["special_ability"]
        )
    )

# sort all gamobjects based on y
gameobjects = [elm for elm in sort_gameobjects(gameobjects)] # create copy of the sorted list

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

# Put ground music
ground_music = pyglet.media.load(data["music"]["location"], streaming=False)

# Setup background
bg_sprite, clouds_sprite = background_setup(win_width, win_height)

# Var init
scrolling = [0, 0]
bg_x_scrolling = 0

# Setup Keyboard
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

def render_update(dt):
    # Make clouds move
    global bg_x_scrolling
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
    # update EVERYTHING about the player
    player.game_update(dt, gameobjects, scrolling, keys, win_width, win_height)
    
    # label update
    coords_label.text = str([round(elm) for elm in player.pos])

    if player.animation == "rewind":
        rewind_labed.text = str(len(player.last_pos))

# Schedule the update and draw functions
pyglet.clock.schedule_interval(game_update, 1/120)
pyglet.clock.schedule_interval(render_update, 1/120)
pyglet.clock.schedule_interval(ground_music.play(), ground_music.duration)

# Start the application
pyglet.app.run()