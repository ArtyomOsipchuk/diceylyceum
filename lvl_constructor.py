class Load_lvl:
    def __init__(self, filename):
        with open(filename, 'r') as mapFile:
            level_map = [line.strip().split('; ') for line in mapFile.readlines()]
        new = []
        for line in level_map:
            a = []
            for i in line:
                if i == '':
                    continue
                if i in '0123456789':
                    i = int(i)
                a.append(i)
            new.append(a)
        self.level_map = new

    def load_level(self):
        return self.level_map
