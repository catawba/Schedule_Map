
from tinydb import TinyDB, Query
db = TinyDB('C:\Users\KyleC\PycharmProjects\Databases\db.json')


class State(object):
    def __init__(self, name, border, color):
        self.name = name
        self.border = border
        self.color = color

    def totalborders(self):
        return len(self.border)


def conflict_check(mapc, con):
    """input m list of map with conflicts
            c list of current map nodes of the same color"""
    for conflict in con:
        for i in mapc:
            if conflict in i:
                print(i.name, conflict)
            else:
                print(i.name, "no conflict")


def map_color(m):
    """input a reverse sorted map list
        output the color for each state"""
    colornum = 1
    maplength = len(map)

    for check in range(maplength):
        idx = 0
        #advance to the first state with no color assigned
        while (map[idx].color != 0):
            idx += 1

        lstconflict = []
        map[idx].color = colornum
        lstconflict.append(map[idx].name)

        for i in map:
            if (i.color == 0):
                cancolor = True
                for c in lstconflict:
                    if c in i.border:
                        cancolor = False

                if cancolor:
                    i.color = colornum
                    lstconflict.append(i.name)
                # else:
                    # go to next node take no action- this node is already colored
                    # pass
            print(i.name, i.color, i.border)
        colornum += 1
        print(colornum)


map = []
m = State(name="KS", border=["NE", "CO", "OK"], color=0)
map.append(m)
m = State(name="OK", border=["TX", "CO", "KS"], color=0)
map.append(m)
m = State(name="TX", border=["OK", "NM"], color=0)
map.append(m)
m = State(name="NM", border=["TX", "CO", "OK", "AZ"], color=0)
map.append(m)
m = State(name="CO", border=["NE", "WY", "OK", "KS", "NM", "UT"], color=0)
map.append(m)
m = State(name="NE", border=["CO", "KS", "WY"], color=0)
map.append(m)
m = State(name="WY", border=["NE", "CO", "UT"], color=0)
map.append(m)
m = State(name="UT", border=["CO", "WY", "AZ"], color=0)
map.append(m)
m = State(name="AZ", border=["UT", "NM"], color=0)
map.append(m)

map.sort(key=lambda c: c.totalborders(), reverse=True)
map_color(map)


