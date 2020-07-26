from math import pi
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class Keyboard(object):
    def __init__(self, status):
        self.status = status
    def listen(self):  # listen to the user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if pygame.mouse.get_pressed()[0]:
                col1 = (pygame.mouse.get_pos()[0] - x_margin) // size
                row1 = (pygame.mouse.get_pos()[1] - y_margin) // size
                # get the position of the square in the 3x9 rectangle
                pos = row1 * col + col1
                # check and update the status
                if self.status[pos]:
                    # notice that this character is chosen
                    print("dont choose again")
                    break
                else:
                    self.status[pos] = True
                    # return
                    return chr(pos + 97)
        return ''
    def draw(self, surface):
        global size, row, col, x_margin, y_margin
        size = 50
        row = 3
        col = 9
        x_margin = 25
        y_margin = 300
        y = y_margin
        for i in range(row + 1):
            pygame.draw.line(surface, (255, 255, 255), (x_margin, y), (x_margin + 9 * size, y))
            y = y + size
        x = x_margin
        for j in range(col + 1):
            pygame.draw.line(surface, (255, 255, 255), (x, y_margin), (x, y_margin + 3 * size))
            x = x + size
        #  draw characters in the square
        font = pygame.font.SysFont('arial', 25)
        for k in range(9):
            if self.status[k]:
                text = font.render(chr(k + 97), True, (255, 0, 0))
            else:
                text = font.render(chr(k + 97), True, (255, 255, 255))
            surface.blit(text, (45 + k * size, 310))  # find a alternative method for '15'
        for k in range(9, 18):
            if self.status[k]:
                text = font.render(chr(k + 97), True, (255, 0, 0))
            else:
                text = font.render(chr(k + 97), True, (255, 255, 255))
            surface.blit(text, (45 + (k - 9) * size, 310 + size))  # find a alternative method for '15'
        for k in range(18, 26):
            if self.status[k]:
                text = font.render(chr(k + 97), True, (255, 0, 0))
            else:
                text = font.render(chr(k + 97), True, (255, 255, 255))
            surface.blit(text, (45 + (k - 18) * size, 310 + 2 * size))  # find a alternative method for '15'

def startKeyboard():
    global key
    key = Keyboard([False] * 26)

class BlankSpace(object):
    global score
    score = 0
    def __init__(self, word, space, lenWord):
        self.word = word  # the word to compare
        self.space = space  # list of character denoting if a character appears in each index
        self.lenWord = lenWord
        self.lenSpace = 0

    def update(self, character):
        # special character ('') inferring nothing is received
        if character == '':
            return True
        result = False
        # iterate through the word
        for index in range(len(self.word)):
            if character == self.word[index]:
                result = True
                self.space[index] = character
                self.lenSpace = self.lenSpace + 1
        return result
    def draw(self, surface):
        # prepare
        number = len(self.word)
        yPos = int(height / 4)
        currentXPos = int(width / 2)
        availLen = int(currentXPos / (2 * number + 1))
        # get to work
        for i in range(number):
            currentXPos += availLen
            # check if draw the horizontal space lines
            if self.word[i] != ' ':
                pygame.draw.line(surface, (255, 255, 255), (currentXPos, yPos), (currentXPos + availLen, yPos))
                # check whether to draw a character on that line
                if self.space[i] != '':
                    font = pygame.font.SysFont('arial', 25)
                    text = font.render(self.space[i], True, (255, 255, 255))
                    surface.blit(text, (currentXPos + 2, yPos - 20))  # find a alternative method for '5'
            currentXPos += availLen

    def checkWin(self):
        if self.lenWord == self.lenSpace:
            return True
        return False

def drawScore(surface,score):
    font = pygame.font.SysFont('arial', 40)
    text = font.render("Score: {}".format(score), True, (255, 255, 255))
    surface.blit(text, (310, 10))

def startBlankSpace():
    # get a random word
    create_list()
    index = random.randint(0, len(list_animal) - 1)
    word = list_animal[index]
    # create instance variable
    list = [''] * len(word)
    # number of characters for the word except for the blank space
    lenn = 0
    for char in word:
        if char != ' ':
            lenn = lenn + 1
    # instantiate the object
    global blank
    blank = BlankSpace(word, list, lenn)

def create_list():
    file = open("animal.txt", "r")
    global list_animal
    list_animal = file.readlines()
    for i in range(len(list_animal)):
        list_animal[i] = list_animal[i][5:-1]
        print(list_animal[0])
    file.close()

class Hang(object):
    def __init__(self, human):
        self.human = human
        self.body = 8
    def change(self, right):
        if not right:
            self.body -= 1
            self.human[self.body] = False
    def draw(self, surface):
        lenEach = int(height / 2 / 3)
        # the length for diameter, the body, and the leg
        radius = int(lenEach / 2)
        x_center = int(width / 4)
        # draw from this  x_center
        white = (255, 255, 255)  # color white
        if self.human[0]:
            # pygame.draw.circle(surface,white)
            pygame.draw.circle(surface, white, (x_center, radius), radius, 1)
        if self.human[1]:
            pygame.draw.line(surface, white, (x_center, radius * 2),
                             (x_center, radius * 2 + lenEach))
        if self.human[2]:
            pygame.draw.line(surface, white, (x_center, radius * 2 + lenEach),
                             (x_center + radius, radius * 2 + lenEach * 2))
        if self.human[3]:
            pygame.draw.line(surface, white, (x_center, radius * 2 + lenEach),
                             (x_center - radius, radius * 2 + lenEach * 2))
        middleY = int(radius * 2 + lenEach / 2)
        if self.human[4]:
            pygame.draw.line(surface, white, (x_center, middleY),
                             (x_center - radius * 2, middleY))
            pygame.draw.line(surface, white, (x_center - radius * 2, middleY),
                             (x_center, radius * 2 + lenEach))
        if self.human[5]:
            pygame.draw.line(surface, white, (x_center, middleY),
                             (x_center + radius * 2, radius * 2))
            y_middle = int(radius / 2)
            y_besides = int(y_middle / 2)
            # draw middle finger
            pygame.draw.line(surface, white, (x_center + radius * 2, radius * 2),
                             (x_center + radius * 2, radius * 2 - y_middle), 2)
            # draw the 2 nearby fingers
            small_pixel = 2
            pygame.draw.line(surface, white, (x_center + radius * 2 - small_pixel, radius * 2),
                             (x_center + radius * 2 - small_pixel, radius * 2 - y_besides), 2)
            pygame.draw.line(surface, white, (x_center + radius * 2 + small_pixel, radius * 2),
                             (x_center + radius * 2 + small_pixel, radius * 2 - y_besides), 2)
        half = int(radius / 2)
        if self.human[6]:
            # left eye
            pygame.draw.circle(surface, white, (x_center - half, radius - half), 2)
            # right eye
            pygame.draw.circle(surface, white, (x_center + half, radius - half), 2)
        if self.human[7]:
            # width is radius, height is radius / 2
            pygame.draw.arc(surface, white, (x_center - half, radius, radius, half), 0, pi)
    def checkLost(self):
        return self.body == 0

def startHang():
    global hang
    hang = Hang([True] * 8)

def redraw(surface):
    surface.fill((0, 0, 0))
    key.draw(surface)
    blank.draw(surface)
    hang.draw(surface)
    drawScore(surface,score)
    pygame.display.update()

def start_game():
    startBlankSpace()
    startKeyboard()
    startHang()

def main():
    # prepare
    global width, height,score
    score = 0
    pygame.init()
    width = 500
    height = width
    frame = pygame.display.set_mode((width, height))
    frame.fill((0, 0, 0))
    # instantiate the game
    start_game()
    # main loop
    flag = True
    while flag:
        # check lose or win every point of time
        if blank.checkWin():
            score += 1
            # announce
            print("Win")
            pygame.time.delay(5000)
            # reset  game
            start_game()
        if hang.checkLost():
            # announce
            score = 0
            print("Lose -> ngu lol")
            print("the word is " + blank.word)
            pygame.time.delay(5000)
            # reset or end game
            start_game()
        inp = key.listen()
        right = blank.update(inp)
        hang.change(right)
        redraw(frame)

main()