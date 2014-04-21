#!/usr/bin/python
import Collision, CalcTools, RidiculousMethods

# this is not unit testing; this is Eric testing.
# Eric testing is unique in that there are no rules.

def rectangle_mask_test():
    pos = CalcTools.PositionVector((5,5),(7,7))
    cfac = Collision.CollisionMaskFactory(pos)
    cmsk = cfac.make_rect_mask((3,3),(0,0))
    rect = cmsk.get_collidables()[0]
    p = rect.get_points()
    fp = rect.get_future_points()
    print(p)
    print(fp)
    rect.add_position_values(p)
    rect.add_position_values(fp)
    print(p)
    print(fp)

def test_lists_to_quads():
    l1 = [(1,2),(2,1),(3,2)]
    l2 = [(3,4),(4,3),(5,4)]
    quads = RidiculousMethods.two_lists_of_points_to_a_bunch_of_quads(l1,l2)
    print(quads)

rectangle_mask_test()
test_lists_to_quads()