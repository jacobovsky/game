import pygame
import numpy as np


pygame.init()
bg = pygame.image.load('sprite_background0.png')
winWidth = 500
winHeight = 600
win = pygame.display.set_mode((winWidth, winHeight))

RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
BLACK = [0, 0, 0]
PRIVILEGE = [255, 255, 255]


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.hitboxCell = []
        self.hitboxCellColor = [GREEN] * 8
        self.hitboxCellDim = 5
        self.hitboxCheckArray = []
        self.queue = [self.x, self.x, self.y, self.y]

        self.isRight = True
        self.isLeft = False
        self.isJump = False
        self.isJump2 = False
        self.isFall = True
        self.justLanded = False
        self.isStanding = False

        self.walkCount = 0
        self.standCount = 0
        self.dashCount = 0

        self.dashCharger = 100

        self.jumpCount = 10
        self.jumpCount2 = 10

    walkRight = []
    for imNumber in range(9):
        walkRight.append(pygame.image.load(f'images/hero/walkRight/Layer 1_sprite_patyczak0{imNumber+1}.png'))
        pass

    walkLeft = []
    for imNumber in range(9):
        walkLeft.append(pygame.image.load(f'images/hero/walkLeft/Layer 1_sprite_patyczak{imNumber+10}.png'))
        pass

    standRight = []
    for imNumber in range(2):
        standRight.append(pygame.image.load(f'images/hero/standing/right/B_{imNumber + 1}.png'))

    standLeft = []
    for imNumber in range(2):
        standLeft.append(pygame.image.load(f'images/hero/standing/left/B_L_{imNumber + 1}.png'))

    def draw(self):
        if not self.isJump and not self.isJump2:
            if self.standCount + 1 >= 20:
                self.standCount = 0
            if self.walkCount + 1 >= 27:
                self.walkCount = 0
            # pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
            if self.isRight and key[pygame.K_RIGHT]:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.isLeft and key[pygame.K_LEFT]:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.isRight:
                win.blit(self.standRight[self.standCount // 10], (self.x, self.y))
                self.standCount += 1
            elif self.isLeft:
                win.blit(self.standLeft[self.standCount // 10], (self.x, self.y))
                self.standCount += 1
            else:
                pass
        else:
            if self.isJump2:
                if self.isRight:
                    win.blit(self.walkRight[0], (self.x, self.y))
                else:
                    win.blit(self.walkLeft[0], (self.x, self.y))
            elif self.isJump:
                if self.isRight:
                    win.blit(self.walkRight[5], (self.x, self.y))
                else:
                    win.blit(self.walkLeft[5], (self.x, self.y))
            else:
                pass
        self.draw_hitbox()

    def set_hitboxcell(self):
        self.hitboxCell = [(self.x + self.width // 4, self.y, self.hitboxCellDim, self.hitboxCellDim),  # upper
                            (self.x + self.width // 4 * 3, self.y, self.hitboxCellDim, self.hitboxCellDim),
                            (self.x + self.width // 4, self.y + self.height - self.hitboxCellDim, self.hitboxCellDim, self.hitboxCellDim),  # lower
                            (self.x + self.width // 4 * 3, self.y + self.height - self.hitboxCellDim, self.hitboxCellDim, self.hitboxCellDim),
                            (self.x, self.y + self.height // 4, self.hitboxCellDim, self.hitboxCellDim),  # on the left side
                            (self.x, self.y + self.height // 4 * 3, self.hitboxCellDim, self.hitboxCellDim),
                            (self.x + self.width - self.hitboxCellDim, self.y + self.height // 4, self.hitboxCellDim, self.hitboxCellDim),  # on the right side
                            (self.x + self.width - self.hitboxCellDim, self.y + self.height // 4 * 3, self.hitboxCellDim, self.hitboxCellDim)]

    def draw_hitbox(self):
        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(win, RED, self.hitbox, 2)
        self.set_hitboxcell()
        for cell in range(len(self.hitboxCell)):
            pygame.draw.rect(win, self.hitboxCellColor[cell], self.hitboxCell[cell], 0)

    def is_standing(self):
        self.queue[0] = self.queue[1]
        self.queue[1] = self.x
        self.queue[2] = self.queue[3]
        self.queue[3] = self.y


class Object(object):
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.filled = 2  # 0 means filled

    def draw(self):
        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(win, self.color, self.hitbox, self.filled)


def is_negative(number):
    if number < 0:
        return -1
    else:
        return 1


fallFactor = 10

pls = [Object(100, 160, 64, 64, BLACK), Object(0, 350, 50, 100, RED), Object(200, 300, 50, 50, PRIVILEGE), Object(250, 300, 70, 70, PRIVILEGE), Object(400, 150, 150, 150, BLUE), Object(0, 550, 500, 150, PRIVILEGE)]
hero = Player(100, 200-64, 64, 64)
hero.hitboxCheckArray = [[0] * 8 for i in range(len(pls))]

clock = pygame.time.Clock()
isGameRunning = True


def is_hero_overlap(platform):
    if hero.x + hero.width + 50 > platform.x and hero.x - 50 < platform.x + platform.width and hero.y - 50 < platform.y + platform.height and hero.y + hero.height + 50 > platform.y:
        return True
    else:
        return False


def is_hero_hitboxcell_overlap():
    for pl in range(len(pls)):
        for cell in range(len(hero.hitboxCell)):
            if hero.hitboxCell[cell][0] + hero.hitboxCell[cell][2] > pls[pl].x and hero.hitboxCell[cell][0] < pls[pl].x + pls[pl].width and hero.hitboxCell[cell][1] < pls[pl].y + pls[pl].height and hero.hitboxCell[cell][1] + hero.hitboxCell[cell][3] > pls[pl].y:
                hero.hitboxCheckArray[pl][cell] = 1  # Red
            else:
                hero.hitboxCheckArray[pl][cell] = 0  # Green


while isGameRunning:
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isGameRunning = False

    key = pygame.key.get_pressed()

    if hero.dashCharger < 100:
        hero.dashCharger += 1
    if ((key[pygame.K_LSHIFT] and hero.dashCount == 0) and hero.dashCharger == 100) or hero.dashCount != 0:
        if hero.isRight:
            hero.x += hero.vel*10
            hero.dashCount += 1
            if hero.x > winWidth-hero.width:
                hero.x = winWidth-hero.width
            if hero.dashCount == 3:
                hero.dashCount = 0
                hero.dashCharger = 0
        elif hero.isLeft:
            hero.x -= hero.vel*10
            if hero.x < 0:
                hero.x = 0
            hero.dashCount += 1
            if hero.dashCount == 3:
                hero.dashCount = 0
                hero.dashCharger = 0
        else:
            pass

    if key[pygame.K_RIGHT] and (hero.x + hero.width) < winWidth:
        hero.x += hero.vel
        hero.isRight = True
        hero.isLeft = False

    elif key[pygame.K_LEFT] and hero.x > 0:
        hero.x -= hero.vel
        hero.isLeft = True
        hero.isRight = False

    if key[pygame.K_SPACE] or hero.isJump:
        hero.isJump = True
        hero.isFall = False
        hero.y = hero.y - is_negative(hero.jumpCount) * hero.jumpCount ** 2 / 2
        hero.jumpCount -= 1
        if hero.jumpCount == 0:
            hero.jumpCount = 10
            hero.isJump = False
            hero.isFall = True

    for pl in range(len(pls)):  # could be useful for optimization
        if is_hero_overlap(pls[pl]):
            pls[pl].filled = 0
        else:
            pls[pl].filled = 2
            pass

    hero.set_hitboxcell()
    is_hero_hitboxcell_overlap()
    cellCheckList = np.sum(hero.hitboxCheckArray, axis=0)

    for i in range(len(cellCheckList)):
        if cellCheckList[i] > 0:
            hero.hitboxCellColor[i] = RED
        else:
            hero.hitboxCellColor[i] = GREEN

    for pl in range(len(pls)):
        extractedHitboxCheckArray = np.array(hero.hitboxCheckArray)
        extractedHitboxCheckArray = extractedHitboxCheckArray[pl, :]
        if extractedHitboxCheckArray[0] == 1 or extractedHitboxCheckArray[1] == 1:
            hero.y = pls[pl].y + pls[pl].height
        elif extractedHitboxCheckArray[2] == 1 or extractedHitboxCheckArray[3] == 1:
            hero.y = pls[pl].y - hero.height
        elif extractedHitboxCheckArray[4] == 1 or extractedHitboxCheckArray[5] == 1:
            hero.x = pls[pl].x + pls[pl].width
        elif extractedHitboxCheckArray[6] == 1 or extractedHitboxCheckArray[7] == 1:
            hero.x = pls[pl].x - hero.width
        else:
            pass

    if hero.isFall and not hero.justLanded:
        hero.y += fallFactor
        hero.justLanded = False

    win.blit(bg, (0, 0))
    for pl in range(len(pls)):
        pls[pl].draw()
    hero.draw()
    pygame.display.update()
