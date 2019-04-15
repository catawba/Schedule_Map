# Mesh the conflict database with the states database
# create states database with class confilict information

#------ This is not finished.  Work on this to build the state_data db so I can run color map.

from tinydb import TinyDB, Query
dbState = TinyDB('C:/Users/KyleC/PyCharmProjects/Databases/state_data.json')
dbConflict = TinyDB('C:/Users/KyleC/PyCharmProjects/Databases/conflict.json')


class State(object):
    def __init__(self, name, border, color):
        self.name = name
        self.border = border
        self.color = color

    def totalborders(self):
        return len(self.border)

for k in dbState:
    print(k)

dbState.close()
dbConflict.close()

