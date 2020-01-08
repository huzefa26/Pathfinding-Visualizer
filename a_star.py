from sortedcontainers import SortedList
from math import sqrt
from time import sleep

MAXINT = 1 << 20


class Astar:
    def __init__(self, master):
        self.master = master
        self.src = self.dest = None

    def G(self, cell):
        # distance from source
        return int(10 * sqrt(pow(self.src.x - cell.x, 2) + pow(self.src.y - cell.y, 2)))

    def H(self, cell):
        # distance from destination
        return int(10 * sqrt(pow(self.dest.x - cell.x, 2) + pow(self.dest.y - cell.y, 2)))

    def get_neighbors(self, cell):
        x, y = cell.x, cell.y
        padosi = []
        if x > 0:
            padosi.append([x - 1, y])
            if y > 0:
                padosi.append([x - 1, y - 1])
            if y < self.master.row_num:
                padosi.append([x - 1, y + 1])
        if y > 0:
            padosi.append([x, y - 1])
        if y < self.master.row_num:
            padosi.append([x, y + 1])
        if x < self.master.col_num:
            padosi.append([x + 1, y])
            if y > 0:
                padosi.append([x + 1, y - 1])
            if y < self.master.row_num:
                padosi.append([x + 1, y + 1])
        return padosi

    def trace(self):
        if self.master.start_cell and self.master.dest_cells:
            OPEN = SortedList(key=lambda cell: self.G(cell) + self.H(cell))
            CLOSED = []
            self.dest = [i for i in self.master.dest_cells][0]
            self.src = self.master.start_cell
            distance = [[MAXINT for c in range(self.master.col_num)] for r in range(self.master.row_num)]
            parent = [[None for c in range(self.master.col_num)] for r in range(self.master.row_num)]
            distance[self.src.y][self.src.x] = 0
            OPEN.add(self.src)
            # distance = 0
            cnt = 6
            while True:
                cell = OPEN.pop(0)
                print(cell.x, cell.y)
                CLOSED.append(cell)
                # distance += self.G(cell) + self.H(cell)
                if cell == self.dest:
                    break
                temp_dist = MAXINT
                for n in self.get_neighbors(cell):
                    temp = self.master.grid[n[1]][n[0]]
                    if temp.typ == 1 or temp in CLOSED:
                        continue
                    f = self.G(temp) + self.H(temp)
                    if distance[n[1]][n[0]] > f and temp not in OPEN:
                        distance[n[1]][n[0]] = f
                        print(temp.x, temp.y, f)
                        parent[n[1]][n[0]] = cell
                        OPEN.add(temp)
                        if temp.typ == 0:
                            temp.draw(cnt)
                # distance += temp_dist
                if cell is not self.dest:
                    cell.draw(5)
                cnt += 1
            cell = self.dest
            while cell != self.src:
                cell = parent[cell.y][cell.x]
                cell.draw(4)
            self.src.draw(2)
        # OPEN.clear()
        # CLOSED.clear()
