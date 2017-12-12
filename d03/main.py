import functools
import math

def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

moves = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))

def spiral2xy(limit):
    space = set([(0,0),(1,0)])
    yield (0, 0)

    if limit == 1:
        return

    yield (1, 0)
    if limit == 2:
        return

    angle = 0
    quarterturn = math.tau / 4

    @functools.lru_cache(None)
    def cos(angle):
        return int(math.cos(angle))

    @functools.lru_cache(None)
    def sin(angle):
        return int(math.sin(angle))

    n = 3
    x, y = 1, 0
    while n <= limit:
        turn = angle + quarterturn
        dx, dy = cos(turn), sin(turn)
        if (x+dx,y+dy) not in space:
            angle = turn
        else:
            dx, dy = cos(angle), sin(angle)
        x += dx
        y += dy
        space.add((x, y))
        yield (x,y)
        n += 1

def position(n):
    for pos in spiral2xy(n):
        pass
    return pos

def get_steps(pos, dest=(0,0)):
    x, y = pos
    steps = 0
    while True:
        if x == dest[0] and y == dest[1]:
            break
        if x < dest[0]:
            x += 1
            steps += 1
        elif x > dest[0]:
            x -= 1
            steps += 1
        if y < dest[1]:
            y += 1
            steps += 1
        elif y > dest[1]:
            y -= 1
            steps += 1
    return steps

def tests():
    expects = { 1: (0,0),
                2: (1,0),
                3: (1,1),
                4: (0,1),
                5: (-1,1),
                6: (-1,0),
                7: (-1,-1),
                8: (0,-1),
                9: (1,-1),
                10: (2,-1),
                11: (2,0),
                12: (2,1),
                13: (2,2),
                14: (1,2),
                15: (0,2),
                16: (-1,2),
                17: (-2,2),
                18: (-2,1),
                19: (-2,0),
                20: (-2,-1),
                21: (-2,-2),
                22: (-1,-2),
                23: (0,-2),
            }

    for n, expected in expects.items():
        pos = position(n)
        assert pos == expected, "n: %s, pos: %s, expected: %s" % (n, pos, expected)

    assert get_steps(position(1)) == 0
    assert get_steps(position(12)) == 3
    assert get_steps(position(23)) == 2
    assert get_steps(position(1024)) == 31

def main():
    tests()

    print("part 1: %s" % (get_steps(position(289326)), ))


if __name__ == "__main__":
    main()
