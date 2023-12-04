# -*- coding: utf-8 -*-
"""
Cannon Defense 

Karter West 

Castle defense game 
Final 

"""

import simpleGe, random, pygame


class Wall(simpleGe.SuperSprite):
    
    def __init__(self, scene):
        super().__init__(scene)
        
        self.setImage("WallPlaceHolder.png")
        self.setPosition((320,300))
        
class BasicEnemy(simpleGe.SuperSprite):
    
    def __init__(self, scene):
        super().__init__(scene)
        
        self.setImage("face.png")
        self.x = 999
        self.setSize(50,50)
        self.y = 20
        self.setBoundAction(self.CONTINUE)
        
    def reset(self):
        self.setDY(0)
        self.y = 20
        self.x = random.randint(20,620)
        
    def kill(self):
        self.setDY(0)
        self.x = 999
        
    def checkEvents(self):    
        if self.x < 900:
            self.addForce(.04, 270)
            
        if self.collidesWith(self.scene.wall):
            self.scene.wallHealth -= 1
            self.setDY(0)
            self.addForce(3, 90) 
        
        if self.collidesGroup(self.scene.CBs):
            self.scene.money += 1
            self.scene.enemiesLeft -= 1
            print(self.scene.enemiesLeft)
            self.kill()
            
        for cb in self.scene.CBs:
            if self.collidesGroup(self.scene.CBs):
                cb.hide()
            
        
class Cannon(simpleGe.SuperSprite):
    
    def __init__(self, scene):
        super().__init__(scene)
        
        self.setImage("CannonPlaceHolder.png")
        self.setSize(60,60)
        self.setPosition((320, 380))
        self.rotateBy(90)
        
    def checkEvents(self):
        if self.scene.isKeyPressed(pygame.K_LEFT):
            self.x -= 5
        if self.scene.isKeyPressed(pygame.K_RIGHT):
            self.x += 5
            
        if self.scene.isKeyPressed(pygame.K_a):
            self.x -= 5
        if self.scene.isKeyPressed(pygame.K_d):
            self.x += 5

class CannonBalls(simpleGe.SuperSprite):
    
    def __init__(self, scene, parent):
        super().__init__(scene)
        
        self.parent = parent
        self.setImage("doughnut.png")
        self.setSize(20,20)
        self.setBoundAction(self.HIDE)
        self.hide()
        
    def fire(self):
        self.show()
        self.setPosition(self.parent.rect.center)
        self.setMoveAngle(self.parent.rotation)
        self.setSpeed(20)
            

class Game(simpleGe.Scene):
    
    def __init__(self):
        super().__init__()
        
        self.background.fill((80,80,80))
        
        self.wall = Wall(self)
        self.cannon = Cannon(self)
        self.NUM_CB = 100
        self.currentCB = 0
        self.CBs = []
        for i in range(self.NUM_CB):
            self.CBs.append(CannonBalls(self, self.cannon))
            
        self.enemies = []
        for i in range(40):
            self.enemies.append(BasicEnemy(self))
        self.enemiesLeft = 5
            
        self.disMoney = simpleGe.Label()
        self.disMoney.text = "Money: 0"
        self.disMoney.center = 50,50
        self.money = 0
        
        self.disWallHealth = simpleGe.Label()
        self.disWallHealth.text = "Health: 100"
        self.disWallHealth.center = 320,300
        self.wallHealth = 100
        
        self.sprites = [self.wall, self.cannon, self.CBs, self.enemies, self.disMoney, self.disWallHealth]
        
    def update(self):
        self.disMoney.text = f"Money: {self.money}"
        self.disWallHealth.text = f"Health: {self.wallHealth}"
        #if self.enemiesLeft == 0:
            
    def doEvents(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.currentCB += 1
                if self.currentCB >= self.NUM_CB:
                    self.currentCB = 0
                self.CBs[self.currentCB].fire()
        
        
def main():
    game = Game()
    game.start()

if __name__ == "__main__":
    main()