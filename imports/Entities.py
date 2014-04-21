import pygame
import magicnums
import DrawTools, CalcTools, Collision

class Entity:
    def __init__(self,pos):
        self.mask = Collision.CollisionMask() # nil mask (won't collide)
        self.pos = CalcTools.PositionVector(pos,(0,0))
        self.netforce = CalcTools.Vector((0,0))
        self.netvel = CalcTools.Vector((0,0))
        self.collided = []
    def add_collided(self,col):
        self.collided.append(col)
    def clear_collided(self):
        self.collided = []
    def render(self,dm):
        return None
    def simulate(self,dt):
        pass
    def get_position(self):
        return self.pos.get_position()
    def get_mask(self):
        return self.mask
    def apply_force(self,newforce):
        self.netforce += newforce
    def prepare_position(self,dt):
        # Modifying displacement vector - not position!
        pos[0] += self.netvel[0]*dt
        pos[1] += self.netvel[1]*dt

class Platform(Entity):
    def __str__(self):
        return "Platform: "+str(self.pos.get_position())
    def __init__(self,pos,dim):
        Entity.__init__(self,pos)

        cf = Collision.CollisionMaskFactory(self.pos)

        self.dim = list(dim)
        self.mask = cf.make_rect_mask(self.dim)
    def render(self,dm):
        borderWidth = 2
        borderColor = magicnums.color['black']
        bdrDrawWidth = self.dim[0] - borderWidth
        bdrDrawHeight = self.dim[1] - borderWidth
        drawRect = pygame.Rect(0,0,bdrDrawWidth,bdrDrawHeight)
        pointList = [drawRect.topleft,drawRect.topright, \
            drawRect.bottomright,drawRect.bottomleft]
        blitSurf = pygame.Surface((self.dim[0],self.dim[1]),
                                  pygame.SRCALPHA, dm.color_depth())
        blitSurf = blitSurf.convert_alpha()
        pygame.draw.polygon(blitSurf,borderColor,pointList,borderWidth)
        return blitSurf, self.get_position()[:2]
class VelocityBox(Entity):
    def __init__(self,pos,vel):
        Entity.__init__(self,pos)

        cf = Collision.CollisionMaskFactory(self.pos)
        
        self.dim = [50,50]
        self.mass = 1 #kg
        self.netvel = vel
        self.mask = cf.make_rect_mask(self.dim)

        #style
        self.fill = (0,0xFF,0)
    def simulate(self,dt):
        if len(self.collided) > 0:
            self.fill = (0xFF,0,0)
            for thing in self.collided:
                print(thing)
        else:
            self.fill = (0,0xFF,0)
        pos = self.pos.get_position()
        pos[0] += self.netvel[0]*dt
        pos[1] += self.netvel[1]*dt
        self.pos.set_position(pos)
    def render(self,dm):
        borderWidth = 2
        borderColor = magicnums.color['black']
        bdrDrawWidth = self.dim[0] - borderWidth
        bdrDrawHeight = self.dim[1] - borderWidth
        drawRect = pygame.Rect(0,0,bdrDrawWidth,bdrDrawHeight)
        pointList = [drawRect.topleft,drawRect.topright, \
            drawRect.bottomright,drawRect.bottomleft]
        blitSurf = pygame.Surface((self.dim[0],self.dim[1]),
                                  pygame.SRCALPHA, dm.color_depth())
        blitSurf = blitSurf.convert_alpha()
        blitSurf.fill(self.fill)
        pygame.draw.polygon(blitSurf,borderColor,pointList,borderWidth)
        return blitSurf, self.get_position()[:2]
