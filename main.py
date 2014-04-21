#!/usr/bin/python
import sys, pygame, traceback, time
import threading
sys.path.append('./imports')
import GameRunner

MAPS_PATH = './data/maps/'

class DisplayManager:
    def __init__(self):
        #DEPRECATED FUNCTION ALIASES
        self.getScreen = self.get_screen
        self.deInit = self.deinit
    def initSafeMode(self):
        self.resolution = self.w, self.h = 800, 600
        self.colorDepth = 32
        pygame.init()
        self.screen = pygame.display.set_mode(self.resolution,pygame.RESIZABLE)
        pygame.display.set_caption("Eric's Attempted Game")
    def deinit(self):
        pygame.display.quit()
        pygame.quit()
    def get_screen(self):
        return self.screen
    def color_depth(self):
        return self.colorDepth

class ControllyThingy(threading.Thread):
    def __init__(self,dm,ins,eth):
        threading.Thread.__init__(self)
        self.dm = dm
        self.ins = ins
        self.eth = eth
    def run(self):
        while True:
            time.sleep(0.3)
            if not self.ins.isAlive():
                self.eth.stopRunning()
                break
        print("STOPPING")
        
        self.dm.deinit()
        time.sleep(5)
        for tup in threading.enumerate():
            print(tup)

class Instance:
    def on_event(self,event):
        if event.type == pygame.QUIT:
            print("MAIN SHOULD DIE NOW")
            self.keepRunning = False
    def test_game(self):
        self.keepRunning = True
        dm = DisplayManager()
        dm.initSafeMode()
        eth = GameRunner.EventThrower()
        ins = GameRunner.GameInstance(dm)
        #controllythingy = ControllyThingy(dm,ins,eth)
        ins.load_map(MAPS_PATH+"test.txt")
        eth.addListener(ins)
        eth.addListener(self)
        while self.keepRunning:
            eth.check_events()
            ins.run_once()
        dm.deinit()
        #ins.start()
        #eth.start()
        #controllythingy.start()
        print("Exiting main thread (MAIN)...")
    def runExit(self):
        print("bye")
    def runMenu(self):
        pass
    def runDev(self):
        pass

if __name__ == "__main__":
    mf = Instance()
    mf.test_game()
