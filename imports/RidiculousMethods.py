
# This is where code that is really difficult to debug goes

def two_lists_of_points_to_a_bunch_of_quads(listOne, listTwo):
    # Lists one and two should be the same length
    quads = []
    for linesegIndex in range(len(listOne)-1):
        quad = listOne[linesegIndex], listOne[linesegIndex+1], \
          listTwo[linesegIndex+1], listTwo[linesegIndex]
        quads.append(quad)
    # one final iteration for the last + first points
    quad = listOne[len(listOne)-1], listOne[0], \
      listTwo[0], listTwo[len(listOne)-1]
    quads.append(quad)

    return quads

def pointSide(a,b,p):
    return (b[0]-a[0])*(p[1]-b[1]) - (b[1]-a[1])*(p[0]-b[0])
