from tkinter import *
# from a_star import A_star
from a_star import Astar
from dijkstra import Dijkstra


class Cell:
    color = ["white", "brown", "green", "crimson", "yellow", "lightyellow", [220, 231, 231]]
    size = None

    def __init__(self, master, x, y):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.x = x
        self.y = y
        self.typ = 0

    def draw(self, typ=0):
        """ yer to the cell to draw its representation on the canvas """
        if self.master:
            self.typ = typ

            xmin = self.x * Cell.size
            xmax = xmin + Cell.size
            ymin = self.y * Cell.size
            ymax = ymin + Cell.size

            if typ > 5:
                c = '#' \
                    + hex(Cell.color[6][0] - 2 * (typ - 5))[2:].zfill(2) \
                    + hex(Cell.color[6][1] - 2 * (typ - 5))[2:].zfill(2) \
                    + hex(Cell.color[6][2] - 2 * (typ - 5))[2:].zfill(2)
                self.master.create_rectangle(xmin, ymin, xmax, ymax, fill=c, outline='blue')
            else:
                self.master.create_rectangle(xmin, ymin, xmax, ymax, fill=Cell.color[typ], outline='black')


class CellGrid(Canvas):
    def __init__(self, master, controller, row_num, col_num, cell_size, *args, **kwargs):
        Canvas.__init__(self, master, width=cell_size * col_num, height=cell_size * row_num, *args, **kwargs)

        self.cell_size = cell_size
        self.row_num = row_num
        self.col_num = col_num

        self.start_cell = None
        self.dest_cells = set()
        self.is_wall_mode = False

        self.path = []

        Cell.size = cell_size
        self.grid = [[Cell(self, column, row) for column in range(col_num)] for row in range(row_num)]

        self.walls = set()

        self.bind("<Button-1>", self.handle_mouse_click)
        self.bind("<B1-Motion>", self.handle_mouse_motion)

        self.draw()

        self.wall_mode_btn = Button(controller,
                                    text="Wall mode : Off",
                                    command=self.toggle_wall_mode,
                                    width=16)
        self.wall_mode_btn.grid(row=0, column=0)

        # Button(controller, text="+", width=3, command=self.increase_cell_size).grid(row=0, column=4, padx=15)
        # Button(controller, text="-", width=3).grid(row=1, column=4, padx=15)

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def _event_coys(self, event):
        r = int(event.y / self.cell_size)
        c = int(event.x / self.cell_size)
        return r, c

    def handle_mouse_click(self, event):
        r, c = self._event_coys(event)
        cell = self.grid[r][c]
        if self.is_wall_mode:
            if cell.typ == 0:
                cell.draw(1)
                self.walls.add(cell)
        elif cell.typ == 1:
            cell.draw()
            self.walls.remove(cell)
        elif cell.typ & 2:  # == 2 or 3
            if cell.typ == 2:
                self.start_cell = None
            else:
                self.dest_cells.remove(cell)
            cell.draw()
        elif cell.typ == 0:
            if self.start_cell:
                cell.draw(3)
                self.dest_cells.add(cell)
            else:
                cell.draw(2)
                self.start_cell = cell

    def handle_mouse_motion(self, event):
        if self.is_wall_mode:
            row, column = self._event_coys(event)
            if self.row_num > row >= 0 and self.col_num > column >= 0:
                cell = self.grid[row][column]
                if cell.typ == 0:
                    cell.draw(1)
                    self.walls.add(cell)

    def toggle_wall_mode(self):
        self.is_wall_mode = not self.is_wall_mode
        if self.is_wall_mode:
            self.wall_mode_btn.config(text='Wall mode: On')
        else:
            self.wall_mode_btn.config(text='Wall mode: Off')

    def reset(self):
        if self.walls:
            # for cell in self.walls:
            #     cell.draw()
            self.walls = set()
        if self.dest_cells:
            # for cell in self.dest_cells:
            #     cell.draw()
            self.dest_cells = set()
        if self.start_cell:
            # self.start_cell.draw()
            self.start_cell = None
        if self.path:
            # for cell in self.path:
            #     cell.draw()
            self.path.clear()
        self.draw()
        self.is_wall_mode = False
        self.wall_mode_btn.config(text='Wall mode: Off')

    # def increase_cell_size(self):
    #     Cell.size += 5
    #     self.cell_size += 5
    #     self.draw()


def reset_xy():
    col_num = getint(x_entry.get())
    row_num = getint(y_entry.get())
    # re-init


def visualize(num_of_cells_hor=20, num_of_cells_ver=15, cell_size=20):
    root = Tk()
    root.geometry(str(num_of_cells_hor * cell_size)
                  + 'x'
                  + str(int(1.2 * num_of_cells_ver * cell_size)))

    control_frame = Frame(root, padx=15, pady=15)  # , bg="#5353ff")
    control_frame.place(relwidth=1, relheight=0.2, relx=0, rely=0)

    grid_frame = Frame(root)
    grid_frame.place(relwidth=1, relheight=0.8, relx=0, rely=0.2)
    cell_grid = CellGrid(grid_frame, control_frame,
                         num_of_cells_ver, num_of_cells_hor,
                         cell_size)
    cell_grid.pack()

    Button(control_frame, text="Clear Grid",
           command=cell_grid.reset, width=16).grid(row=1, column=0)

    Label(control_frame, text="X: ", bd=0, width=5, anchor=E) \
        .grid(row=0, column=2, padx=5)
    x_entry = Entry(control_frame, width=5)
    x_entry.grid(row=0, column=3)

    Label(control_frame, text="Y: ", bd=0, width=5, anchor=E) \
        .grid(row=1, column=2, padx=5)
    y_entry = Entry(control_frame, width=5)
    y_entry.grid(row=1, column=3)

    Button(control_frame, text="Reset\nGrid", command=reset_xy) \
        .grid(row=0, column=4, rowspan=2, padx=10)
    # clear_grid_btn.pack()

    # root.mainloop()

    return root


def setup_algos(root):
    controller = root.winfo_children()[0]
    cell_grid = root.winfo_children()[1].winfo_children()[0]

    a_star = Astar(cell_grid)
    Button(controller, text="A*", width=10, command=a_star.trace).grid(row=0, column=8)

    dijkstra = Dijkstra(cell_grid)
    Button(controller, text="Dijkstra", width=10, command=dijkstra.trace).grid(row=1, column=8)


if __name__ == "__main__":
    root = visualize()
    setup_algos(root)
    root.mainloop()
