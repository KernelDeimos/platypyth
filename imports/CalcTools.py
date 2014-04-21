import math
import Misc
def sort_length_asc(*lists):
    return sorted(lists, key=lambda lis: len(lis))

class Vector:
    def __init__(self, comps = False):
        self.components = comps or [0]
    def __add__(vec1, vec2):
        smlLis, bigLis =  sort_length_asc(vec1, vec2)
        newcomps = []
        sLen = len(smlLis)
        for x in range(sLen):
            newcomps.append(vec1[x] + vec2[x])
        for x in range(len(bigLis) - sLen):
            newcomps.append(bigLis[x])
        return Vector(newcomps)
    def __sub__(vec1, vec2):
        vec2 = vec2.get_negative
        return vec1 + vec2
    def __len__(self):
        return len(self.components)
    def __getitem__(self, key):
        return self.components[key]
    def __setitem__(self, key, val):
        self.components[key] = val
    
    def get_negative(self):
        newcomps = []
        for comp in self.components:
            newcomps.append(-comp)
        return Vector(newcomps)
    def magnitude(self):
        sumsquared = 0
        for val in self.components:
            sumsquared += val**2
        return math.sqrt(sumsquared)
class PositionVector(Vector):
    def __str__(self):
        return "<<<POSITION VECTOR: "+str(self.get_position()[0])+","+str(self.get_position()[1])+">>>"
    def __init__(self, pos, comps=False, relpos=None):
        Vector.__init__(self, comps)
        pos = list(pos)
        while len(pos) < len(comps):
            pos.append(0)
        self.position = pos
        self.relptr = relpos
    def get_position(self):
        retPosition = []
        if self.relptr != None:
            smlPos, bigPos = sort_length_asc(self.position, self.relptr.get_position())
            retPosition = [item for item in bigPos]
            for k,item in enumerate(smlPos):
                retPosition[k] += item
        else:
            retPosition = self.position
        return retPosition
    def get_vector_components(self,expectedLength = None):
        """get vector component list of [expectedLength] dimensions"""
        retVector = []
        if self.relptr != None:
            smlVec, bigVec = sort_length_asc(self.components, self.relptr.get_vector_components())
            retVector = [item for item in bigVec]
            for k,item in enumerate(smlVec):
                retVector[k] = item
        else:
            retVector = self.components
        if expectedLength != None:
            if len(retVector) > expectedLength:
                retVector = retVector[:expectedLength]
            else:
                while len(retVector) < expectedLength:
                    retVector.append(0)
        return retVector
    def set_position(self,newpos):
        self.position = newpos

class LineSeg:
    @staticmethod
    def point_side(A,B,P):
        return (B[0]-A[0])*(P[1]-B[1]) - (B[1]-A[1])*(P[0]-B[0])
    def __init__(self,p1,p2):
        self.points = [p1,p2]
    def __getitem__(self,pi):
        return self.points[pi]
    def check_collision(line1,line2):
        # these values indicate which side of a line segment a point is on.
        line_one_point_C = LineSeg.point_side(line1[0],line1[1],line2[0])
        line_one_point_D = LineSeg.point_side(line1[0],line1[1],line2[0])
        line_two_point_A = LineSeg.point_side(line2[0],line2[1],line1[0])
        line_two_point_B = LineSeg.point_side(line2[0],line2[1],line1[1])
        if (line_one_point_C != line_one_point_D) and (line_two_point_A != line_two_point_B):
            return True
        return False