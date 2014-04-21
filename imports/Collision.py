import pygame
import CalcTools, RidiculousMethods
# I'm going to call these triplets of double-quotes 'hexaquotes' :D

class CollisionMaskPart:
    def __init__(self,pos):
        if isinstance(pos,CalcTools.PositionVector):
            self.pos = pos
        else: # TODO: REMOVE THIS ALTERNATIVE
            self.pos = CalcTools.PositionVector(pos,(0,0,0))
        self.type="none"
    def get_type(self):
        return self.type
    def get_position(self):
        return self.pos.get_position()[:2]
    def set_position_vector(self, pos):
        self.pos = pos

class CollisionPolygon(CollisionMaskPart):
    def __init__(self,pos,*points):
        CollisionMaskPart.__init__(self,pos)
        self.points = points
        self.type="polygon"
        # RENAMED FUNCTIONS
        self.get_point_array = self.get_points
    def get_points(self): # should be renamed "get_points"
        return self.points[:]
    def get_future_points(self):
        """returns points after a vector
        (code is extensible for nth dimension objects)
        """
        nDim = 2
        deltaComps = self.pos.get_vector_components(nDim)
        futurePoints = []
        for point in self.points:
            newpoint = [point[i]+deltaComps[i] for i in range(nDim)]
            futurePoints.append(newpoint)
        return futurePoints[:]#justtobesafe
    def add_position_values(self,coordList):
        position = self.pos.get_position()
        for coord in coordList:
            for k in range(len(coord)):
                if k < len(position):
                    coord[k] += position[k]
                else:
                    break
        return coordList

class CollisionRectangle(CollisionMaskPart):
    def __init__(self,pos,dim):
        CollisionMaskPart.__init__(self,pos)
        self.dim = dim
        self.type="rectangle"
    def get_dimensions(self):
        return self.dim

class CollisionMask:
    def __init__(self, pos=(0,0)):
        self.parts = []
        self.pos = pos
    def add_collidable(self, part):
        self.parts.append(part)
    def get_collidables(self):
        return self.parts
    def test_collision(m1,m2):
        for c1 in m1.get_collidables():
            for c2 in m2.get_collidables():
                t1, t2 = c1.get_type(), c2.get_type()
                if t1 == "rectangle" and t2 == "rectangle":
                    # THIS IS INCOMPLETE SILLY STUFF (might be removed)
                    print(c1.get_position())
                    rect1 = pygame.Rect(c1.get_position(), c1.get_dimensions())
                    rect2 = pygame.Rect(c2.get_position(), c2.get_dimensions())
                    if rect1.colliderect(rect2):
                        return True
                elif t1 == "polygon" and t2 == "polygon":
                    pointLists = [0,0,0,0]
                    pointLists = [c1.get_points(), c1.get_future_points(),
                      c2.get_points(), c2.get_future_points()]
                    for k in range(2):
                        c1.add_position_values(pointLists[k])
                    for k in range(2,4):
                        c2.add_position_values(pointLists[k])
                    lineSegList = [[],[]]
                    for x in range(len(pointLists[0])):
                        x2 = x + 1
                        if x2 == len(pointLists[0]): x2=0
                        lineSegList[0].append(CalcTools.LineSeg(pointLists[0][x],pointLists[0][x2]))
                        lineSegList[0].append(CalcTools.LineSeg(pointLists[1][x],pointLists[1][x2]))
                        lineSegList[0].append(CalcTools.LineSeg(pointLists[0][x],pointLists[1][x]))
                    for x in range(len(pointLists[2])):
                        x2 = x + 1
                        if x2 == len(pointLists[2]): x2=0
                        lineSegList[1].append(CalcTools.LineSeg(pointLists[2][x],pointLists[2][x2]))
                        lineSegList[1].append(CalcTools.LineSeg(pointLists[3][x],pointLists[3][x2]))
                        lineSegList[1].append(CalcTools.LineSeg(pointLists[2][x],pointLists[3][x]))
                    for line1 in lineSegList[0]:
                        for line2 in lineSegList[1]:
                            if line1.check_collision(line2):
                                return True
        return False

class CollisionMaskFactory:
    def __init__(self,pos=None):
        self.pos = pos
    def make_rect_mask(self,dim,pos=(0,0)):
        if self.pos != None:
            posToUse = CalcTools.PositionVector(pos,(0,0,0),self.pos)
        else:
            posToUse = CalcTools.PositionVector(pos,(0,0,0))
        cm = CollisionMask(self.pos)
        cr = CollisionRectangle(posToUse,[dim[0],dim[1]])
        cp = CollisionPolygon(posToUse,[0,0],[0,dim[1]],[dim[0],dim[1]],[dim[0],0])
        cm.add_collidable(cr)
        cm.add_collidable(cp)
        return cm
