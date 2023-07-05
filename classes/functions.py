def range_from_object(pos: list[int|float]|list[int], size: list[int|float]|list[int]) -> list[list[int]]:
    posInt: list[int] = [round(pos[0]), round(pos[1])]
    sizeInt: list[int] = [round(size[0]), round(size[1])]

    return [list(range(posInt[0],posInt[0]+sizeInt[0]+1)), list(range(posInt[1],posInt[1]+sizeInt[1]+1))]