#! python

import sys
import matplotlib
import copy

class Board():
    def __init__(self, points=None):
        if not points: # init points with 0
            self.points = []
            for i in range(9):
                self.points.append([0,0,0,0,0,0,0,0,0])
        else:
            self.points = copy.copy(points)

    def setVal(self, row, col, val):
        self.points[row][col] = val

    def _drawRow(self, ix):
        row = [ str(x) for x in self.getRow(ix) ]
        print(" {} | {} | {}".format(" ".join(row[0:3]), " ".join(row[3:6]), " ".join(row[6:9])))

    def draw(self):
        for row in range(9):
            if row in [0, 3, 6]:
                print(" ---------------------")
            self._drawRow(row)
        print(" ---------------------")

    def isComplete(self):
        for row in range(9):
            for col in range(9):
                if self.points[row][col] == 0:
                    return False
        return True

    def getRow(self, row):
        return self.points[row]

    def getCol(self, col):
        return [ self.points[x][col] for x in range(9)]

    def getSquareValues(self, row, col):
        if row > 5:
            rows = [6, 7, 8]
        elif row > 2:
            rows = [3, 4, 5]
        else:
            rows = [0, 1, 2]

        if col > 5:
            cols = [6, 7, 8]
        elif col > 2:
            cols = [3, 4, 5]
        else:
            cols = [0, 1, 2]

        values = []
        for r in rows:
            for c in cols:
                val = self.points[r][c]
                if val:
                    values.append(val)
        return values

    def getAllowedValues(self, row, col):
        assert self.points[row][col] == 0
        found = self.getCol(col)
        found.extend(self.getRow(row))
        found.extend(self.getSquareValues(row, col))
        allowed = [ x for x in range(1, 10) if not x in found]
        # print("got allowed values for pos {}:{}  -> {}".format(row, col, allowed))
        return allowed

    def solve(self):
        if self.isComplete():
            return self
        for r in range(9):
            for c in range(9):
                val = self.points[r][c]
                if val:
                    continue
                else:
                    candidates = self.getAllowedValues(r, c)
                    for cand in candidates:
                        self.setVal(r, c, cand)
                        if self.solve():
                            return self
                        else:
                            self.setVal(r, c, 0)
                            continue
                    # print("bummer! Backtracking ...")
                    return None
                    
        return None

def main(argv):
    board = Board()
    points = [ 
        [0,1,3],
        [1,3,1],
        [1,4,9],
        [1,5,5],
        [2,2,8],
        [2,7,6],
        [3,0,8],
        [3,4,6],
        [4,0,4],
        [4,3,8],
        [4,8,1],
        [5,4,2],
        [6,1,6]]

    for p in points:
        board.setVal(p[0], p[1], p[2])

    # board.setVal(1,3,3)
    # board.setVal(1,4,4)
    # print(board.getAllowedValues(1,5))
    board.draw()
    b = board.solve()
    if b:
        b.draw()
    else:
        print("cannot solve")

if __name__ == "__main__":
    main(sys.argv)
