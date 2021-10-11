class Wall:
    def __init__(self, x, y, t):
        self.key = (x, y, t)
        self.neighbor = []
        self.is_draw = True