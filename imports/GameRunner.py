import threading, time, pygame
import magicnums
import DrawTools, CalcTools, Factories

class EventThrower (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.listeners = []
        self.loopDelay = 0.001
    def addListener(self,lis):
        self.listeners.append(lis)
    def check_events(self):
        evlist = pygame.event.get()
        for event in evlist:
            if event.type == 1 \
               or event.type == 4 \
               or event.type == 16 \
               or event.type == 17:
                continue
            if event.type == pygame.QUIT:
                print("Sending quit event to all listeners!")
            for lis in self.listeners:
                lis.on_event(event)
    def run(self):
        print("Starting event thread...")
        self.keepRunning = True
        while self.keepRunning:
            self.check_events()
            time.sleep(self.loopDelay)
        print("Exiting event thread...")
        return
    def stopRunning(self):
        self.keepRunning = False



class GameInstance(threading.Thread):
    def __init__(self,dm):
        threading.Thread.__init__(self)
        self.dm = dm
        self.entities = [] # "everything" array
        self.entities_collidable = []
        self.eventQueue = []
        self.clock = pygame.time.Clock()
        pass
    def load_map(self,filename):
        # Returns (bool success,string[] warnings)
        fileLines = []
        warnings = []

        platfac = Factories.PlatformFactory()

        try:
            with open(filename,'r') as f:
                fileLines = f.readlines()
        except:
            print("Error loading map :/")
            return (False,[])
        for ln,line in enumerate(fileLines):
            lns = "Line "+str(ln)+": "
            data = line.split()
            if len(data) < 1:
                continue
            if data[0] == "EOF":
                break
            if data[0] == "platform":
                if len(data) != 5:
                    warnings.append(lns+"Invalid argument count")
                    #TODO: Add tabbed additional info
                    continue
                nums = []
                try:
                    for val in data[1:]:
                        nums.append(float(val))
                except ValueError:
                    warnings.append(lns+"Invalid argument type")
                obj = platfac.getNewPlatform((nums[0],nums[1],0),(nums[2],nums[3]))
                self.entities.append(obj)
                self.entities_collidable.append(obj)
            elif data[0] == "velbox":
                if len(data) != 5:
                    warnings.append(lns+"Invalid argument count")
                    #TODO: Add tabbed additional info
                    continue
                nums = []
                try:
                    for val in data[1:]:
                        nums.append(float(val))
                except ValueError:
                    warnings.append(lns+"Invalid argument type")
                obj = platfac.getNewVelbox((nums[0],nums[1],0),(nums[2],nums[3]))
                self.entities.append(obj)
                self.entities_collidable.append(obj)


        return (True,warnings)
        pass
    def draw(self):
        screen = self.dm.getScreen()
        screen.fill(magicnums.color['white'])

        self.entities = sorted(self.entities, key=lambda entity: entity.get_position()[2])
        for entity in self.entities:
            rendSurf, coords = entity.render(self.dm)
            if rendSurf is not None:
                self.dm.get_screen().blit(rendSurf, coords)

        pygame.display.flip()
    def check_events(self):
        for event in self.eventQueue:
            if event.type == pygame.QUIT:
                print("INS SHOULD DIE NOW")
                self.keepRunning = False
    def check_collisions(self):
        for item in self.entities_collidable:
            item.clear_collided()
        for k1,item1 in enumerate(self.entities_collidable):
            for k2,item2 in enumerate(self.entities_collidable):
                if k1==k2: continue
                m1, m2 = item1.get_mask(), item2.get_mask()
                if m1.test_collision(m2):
                    item1.add_collided(item2)
                    item2.add_collided(item1)
    def simulate(self):
        for entity in self.entities:
            entity.simulate(self.dt)
    def run_once(self):
        self.dt = self.clock.tick(60)
        self.simulate()
        self.check_collisions()
        self.draw()
        self.check_events()
    def run(self):
        print("Starting game thread (INS)...")
        self.keepRunning = True
        while self.keepRunning:
            self.run_once()
        self.clean()
    def clean(self):
        print("Exiting game thread (INS)...")
        return
    def on_event(self,event):
        self.eventQueue.append(event)
        pass
