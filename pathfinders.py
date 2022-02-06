import moves

def circular(m):
    if len(m.aux['path']) == 1: # not enough data to determine direction, provide both options
        return moves.diradj(m.dir)
    else: # enough data, extrapolate
        fullpath = [m.src] + m.aux['path'] # we might need src in this case; include

        dirp = moves.sublocs(fullpath[-2], fullpath[-3]) # previous dir
        dirc = m.dir # current dir
        adjs = moves.diradj(dirc) # get adjacent dirs (of which dirp should be one)
        if adjs[0] == dirp:
            # print(dirc, adjs[1])
            return [adjs[1]]
        else:
            # print(dirc, adjs[0])
            return [adjs[0]]
        # basically, find where you are in the circle, and also which direction to go (requires 2 directions, or 3 points on a path)


# crooked pathfinder (zigzag)
def crooked(m):
    if len(m.aux['path']) == 1: # not enough data to determine direction, provide both options
        return moves.diradj(m.dir)
    else: # enough data, extrapolate
        fullpath = [m.src] + m.aux['path'] # we might need src in this case; include
        dirp = moves.sublocs(fullpath[-2], fullpath[-3]) # previous dir
        return [dirp] # crooked movement is a back and forth, so the previous direction is the next one


def idem(m):
    return [m.dir]

