import heapq

class Node:

    def __init__(self, x, y, father, target, cost=1):
        self.x = x
        self.y = y

        self.father = father

        self.prev = father.prev + cost if father else 0
        self.dist = (target.y-y)+(target.x-x) if target else 0

        self.heu = self.prev+self.dist

    def __lt__(self, other):
        return self.heu < other.heu


class Pathfind():
    _UNDEF = -3
    _OPENED = -2
    _CLOSED = -1
    _COLLISION = 0

    _MAX_TICKS = 1000


    def __init__(self, matrix, borders, collidable_diagonals=True, max_ticks=_MAX_TICKS):
        self._matrix = matrix
        self._borders = borders

        self._bw = borders.width
        self._bh = borders.height

        self._allow_diagonals = collidable_diagonals

        self._max_ticks = max_ticks if max_ticks != None else _MAX_TICKS*10
    
    
    def search(self, x1, y1, x2, y2):
        pfc = Pathfind._COLLISION

        if self._matrix[y2][x2] > pfc:
            last = Node(x2, y2, None, None)
            start = Node(x1, y1, None, last)

            open_list = [ (start.heu, start) ]
            closed_dict = {}

            npath = None

            found = False
            current = None

            ticks = self._max_ticks

            while len(open_list) > 0:
                current = heapq.heappop(open_list)[1]
                cx = current.x
                cy = current.y

                if cx == x2 and cy == y2:
                    found = True
                    break
                elif ticks <= 0:
                    break

                closed_dict[(cx,cy)] = (current, Pathfind._CLOSED)
                ticks -= 1

                for nx in range( max(cx-1,0), min(cx+2,self._bw), 1):
                    for ny in range(max(cy-1,0), min(cy+2,self._bh), 1):
                        dx = nx - cx
                        dy = ny - cy
                        cost = self._matrix[ny][nx]

                        if cost > pfc and (dx != 0 or dy != 0):
                            non_diag = (dx==0 or dy==0)
                            if non_diag or (self._matrix[ny][cx] > pfc and self._matrix[cy][nx] > pfc):
                                tup = (nx,ny)
                                state = closed_dict.get(tup, (None,Pathfind._UNDEF))
                                if state[1] < Pathfind._CLOSED:
                                    vnode = Node(nx, ny, current, last, cost if non_diag else cost*1.4)
                                    if state[1] == Pathfind._UNDEF or vnode.prev < state[0].prev:
                                        heapq.heappush( open_list, ( vnode.heu, vnode ) )
                                        closed_dict[tup] = (vnode, Pathfind._OPENED)

        if found:
            npath = []
            while current.father != None:
                npath.append( (current.x, current.y) )
                current = current.father


        return npath