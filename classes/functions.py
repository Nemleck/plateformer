import pyglet
from pyglet import gl

def range_from_object(pos: list[int|float]|list[int], size: list[int|float]|list[int]) -> list[list[int]]:
    posInt: list[int] = [round(pos[0]), round(pos[1])]
    sizeInt: list[int] = [round(size[0]), round(size[1])]

    return [list(range(posInt[0],posInt[0]+sizeInt[0]+1)), list(range(posInt[1],posInt[1]+sizeInt[1]+1))]

def sort_gameobjects(gameobjects):
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
    
    return result

def background_setup(win_width, win_height):
    bg_img = pyglet.image.load("sources/plateform/background.png")
    bg_sprite = pyglet.sprite.Sprite(bg_img, 0, 0)
    bg_sprite.scale_x = win_width
    bg_sprite.scale_y = win_height

    clouds_img = pyglet.image.load("sources/plateform/clouds.png")
    clouds_sprite = pyglet.sprite.Sprite(clouds_img, 0, 0)
    clouds_sprite.scale = 2
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

    return bg_sprite, clouds_sprite