import api
import time


class POS:
    def __init__(self, col, row):
        self.__col = col
        self.__row = row

    def get_col(self):
        return self.__col

    def set_col(self, col):
        self.__col = col

    def get_row(self):
        return self.__row

    def set_row(self, row):
        self.__row = row

    def __eq__(self, other):
        return (self.__col == other.col and self.__row == other.row)

    row = property(get_row, set_row)
    col = property(get_col, set_col)


FORWARD = 0
RIGHT = 1
LEFT = 2
N = POS(0, +1)
S = POS(0, -1)
W = POS(-1, 0)
E = POS(+1, 0)
NUM_ROWS = 80
NUM_COLS = 80

TARGET = 4
BLOCK = 1
OBJECT = 0
EMPTY = 3
MAX_DEPTH = 7
INF = 9999

pos = POS(40, 40)
tankdir = POS(1, 0)

mincol = NUM_COLS
minrow = NUM_ROWS
maxcol = 0
maxrow = 0


def update_dir(direction, turn):
    if direction == N and turn == LEFT:
        return W
    if direction == E and turn == LEFT:
        return N
    if direction == W and turn == LEFT:
        return S
    if direction == S and turn == LEFT:
        return E

    if direction == N and turn == RIGHT:
        return E
    if direction == S and turn == RIGHT:
        return W
    if direction == E and turn == RIGHT:
        return S
    if direction == W and turn == RIGHT:
        return N


class Solution:
    def __init__(self):
        self.coutner = 0
        self.fuelNow = api.current_fuel()
        self.fuelBefore = api.current_fuel()
        # If you need initialization code, you can write it here!
        # Do not remove.
        self.Map = [[OBJECT for x in range(NUM_ROWS)] for y in range(NUM_COLS)]
        self.visit = [[[] for x in range(NUM_ROWS)] for y in range(NUM_COLS)]

    def pos_forward(self, posz, direction, step):
        return POS(posz.col + (direction.col * step), posz.row + (direction.row * step))

    def NearestCost(self, posx, direction, cost, search_depth):
        # print("NearestCost", posx.col,posx.row, direction.col, direction.row, search_depth)

        if self.Map[posx.col][posx.row] == BLOCK:
            return (cost + INF, FORWARD)
        if (search_depth == 0):
            if self.Map[posx.col][posx.row] == EMPTY:
                return (cost + 1, FORWARD)
            if self.Map[posx.col][posx.row] == TARGET:
                return (cost - 10, FORWARD)
            elif self.Map[posx.col][posx.row] == OBJECT:
                return (cost, FORWARD)
        else:  # Not last move
            if (self.Map[posx.col][posx.row] == OBJECT):
                return (cost + 1, FORWARD)
            elif (self.Map[posx.col][posx.row] == TARGET):
                return (cost - 10, FORWARD)
            elif (self.Map[posx.col][posx.row] == EMPTY):
                f_len = 0
                r_len = INF + 1
                l_len = INF + 2
                fp = self.pos_forward(posx, direction, 1)

                (f_len, f_move) = self.NearestCost(fp, direction, cost + 1, search_depth - 1)
                col,row= (direction.col, direction.row)
                if ( (col,row) in self.visit[fp.col][fp.row]) :
                    f_len = f_len + INF
                f_len = f_len + 1
                (l_len, l_move) = self.NearestCost(posx, update_dir(direction, LEFT), cost + 1, search_depth - 1)
                l_len = l_len + 1
                (r_len, r_move) = self.NearestCost(posx, update_dir(direction, RIGHT), cost + 1, search_depth - 1)
                r_len = r_len + 1

        # print ("decision:", "forward =", f_len, "left=", l_len, "right=", r_len)
        if (f_len <= l_len and f_len <= r_len):
            return (f_len, FORWARD)
        elif (l_len <= f_len and l_len <= r_len):
            return (l_len, LEFT)
        elif (r_len <= f_len and r_len <= l_len):
            return (r_len, RIGHT)

    def update(self):
        """
        Executes a single step of the tank's programming. The tank can only
        move, turn, or fire its cannon once per turn. Between each update, the
        tank's engine remains running and consumes 1 fuel. This function will be
        called repeatedly until there are no more targets left on the grid, or
        the tank runs out of fuel.
        """
        global tankdir
        global maxcol, maxrow, mincol, minrow

        self.Map[pos.col][pos.row] = EMPTY
        for i in range(20, 60):
            for j in range(20, 60):
                if (i == pos.col and j == pos.row):
                    print(9 - self.Map[i][j], end='')
                else:
                    print(self.Map[i][j], end='')
            print("")
        # for i  in range(20 , 60) :
        #     for j in range(20, 60) :
        #         if (i== pos.col and j==pos.row ):
        #             print(9-self.visit[i][j], end='')
        #         else:
        #             print(self.visit[i][j], end='')
        #     print("")
        if (api.identify_target()):
            front_object = TARGET
        else:
            front_object = BLOCK

        # Todo: Write your code here!
        # front (no turn)
        tempdir = tankdir
        for i in range(1, api.lidar_front()):
            self.Map[pos.col + (i * tempdir.col)][pos.row + (i * tempdir.row)] = EMPTY
        tmpcol = pos.col + (api.lidar_front() * tempdir.col)
        tmprow = pos.row + (api.lidar_front() * tempdir.row)
        if self.Map[tmpcol][tmprow] != BLOCK:
            self.Map[tmpcol][tmprow] = front_object

        # back (turn twice)
        tempdir = update_dir(update_dir(tankdir, RIGHT), RIGHT)
        for i in range(1, api.lidar_back()):
            self.Map[pos.col + (i * tempdir.col)][pos.row + (i * tempdir.row)] = EMPTY
        tmpcol = pos.col + (api.lidar_back() * tempdir.col)
        tmprow = pos.row + (api.lidar_back() * tempdir.row)
        if self.Map[tmpcol][tmprow] != BLOCK:
            self.Map[tmpcol][tmprow] = OBJECT

        tempdir = update_dir(tankdir, LEFT)
        for i in range(1, api.lidar_left()):
            self.Map[pos.col + (i * tempdir.col)][pos.row + (i * tempdir.row)] = EMPTY
        tmpcol = pos.col + (api.lidar_left() * tempdir.col)
        tmprow = pos.row + (api.lidar_left() * tempdir.row)
        if self.Map[tmpcol][tmprow] != BLOCK:
            self.Map[tmpcol][tmprow] = OBJECT

        tempdir = update_dir(tankdir, RIGHT)
        for i in range(1, api.lidar_right()):
            self.Map[pos.col + (i * tempdir.col)][pos.row + (i * tempdir.row)] = EMPTY
        tmpcol = pos.col + (api.lidar_right() * tempdir.col)
        tmprow = pos.row + (api.lidar_right() * tempdir.row)
        if self.Map[tmpcol][tmprow] != BLOCK:
            self.Map[tmpcol][tmprow] = OBJECT

        ## update surrounding walls as blocker
        for i in range(0, NUM_COLS):
            for j in range(0, NUM_ROWS):
                if (self.Map[i][j] == EMPTY):
                    if i < mincol:
                        mincol = i
                    if i > maxcol:
                        maxcol = i
                    if j < minrow:
                        minrow = j
                    if j > maxrow:
                        maxrow = j

        if maxcol - mincol == 9:
            for j in range(0, NUM_ROWS):
                self.Map[mincol - 1][j] = BLOCK
                self.Map[maxcol + 1][j] = BLOCK
            for i in range(0, NUM_COLS):
                self.Map[i][minrow - 1] = BLOCK
                self.Map[i][maxrow + 1] = BLOCK
        if maxcol - mincol == 19:
            for j in range(0, NUM_ROWS):
                self.Map[mincol - 1][j] = BLOCK
                self.Map[maxcol + 1][j] = BLOCK
            for i in range(0, NUM_COLS):
                self.Map[i][minrow - 1] = BLOCK
                self.Map[i][maxrow + 1] = BLOCK

        # print( "position", pos.col, pos.row, tankdir.col, tankdir.row,
        #    "lf", api.lidar_front(), "lb", api.lidar_back(), "ll", api.lidar_left(), "lr", api.lidar_right())
        if (api.identify_target() and api.lidar_front() < 6):
            api.fire_cannon()
        else:
            maxdep = MAX_DEPTH  # api.current_fuel()
            (dist, move) = self.NearestCost(pos, tankdir, 0, maxdep)
            # print("best move", (dist, move))
            if (move == FORWARD):
                api.move_forward()
                self.visit[pos.col][pos.row].extend((tankdir.col, tankdir.row))
                x = self.pos_forward(pos, tankdir, 1)
                pos.col = x.col
                pos.row = x.row

            if (move == RIGHT):
                tankdir = update_dir(tankdir, RIGHT)
                api.turn_right()
            if (move == LEFT):
                tankdir = update_dir(tankdir, LEFT)
                api.turn_left()
