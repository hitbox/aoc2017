import math

def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

moves = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))

def spiral2xy(num):
    x, y = (0, 0)
    yield x, y

    prev = (x, y)


    possibles = list( (x+dx,y+dy) for dx,dy in moves if (dx,dy) != prev)
    print(possibles)
    possibles = list( (pos, distance(pos, (0,0))) for pos in possibles)
    print(possibles)

    possibles = sorted(possibles, key=lambda posdist: posdist[1])
    print(possibles)

def tests():
    from pprint import pprint as pp
    for whatever in spiral2xy(23):
        print(whatever)

def main():
    tests()

if __name__ == "__main__":
    main()
