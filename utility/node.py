class Node:
    def __init__(self, name, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.name = name

    def set_posX(self, x):
        self.pos_x = x

    def set_posY(self, y):
        self.pos_y = y

    def get_posX(self):
        return self.pos_x

    def get_posY(self):
        return self.pos_y

    def get_name(self):
        return self.name
