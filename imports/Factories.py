import pygame
import DrawTools, CalcTools, Entities

class PlatformFactory:
    def __init__(self):
        pass
    def getNewPlatform(self,pos,dim):
        plat = Entities.Platform(pos,dim)
        return plat
    def getNewVelbox(self,pos,vel):
        plat = Entities.VelocityBox(pos,vel)
        return plat
