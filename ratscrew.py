############################################################################################
#
# Project           : Simple Mutated Classic VG in Pygame
#
# Program Name      : ratscrew.py
#
# Author            : diegofranchi
# CWID              : 889894283
#
# Date Created      : 20180328
#
# Purpose           : practice programming a game and mutate it
#
# Revision History  :
#
# Date        Author        Ref     Revision (Date in YYYMMDD format)
# 20180328    diegofranchi  1       Created game skeleton using classes
# 20180330    diegofranchi  2       Created Menu class and functions
# 20180331    diegofranchi  3       Created Game class with trun/slap/win logic
# 20180401    diegofranchi  4       Polished game, squashed bugs, added extra features
#
############################################################################################

import pygame
import time
from random import shuffle

pygame.init()
pygame.mixer.init()

width = 800
height = 600

black = (0,0,0)
white = (255,255,255)
highlight = (243,243,21)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('RATSLAP v1.4.20')
clock = pygame.time.Clock()
pygame.mixer.music.load('sounds/menu_song.ogg')
shuffling = pygame.mixer.Sound('sounds/shuffling.ogg')
slap = pygame.mixer.Sound('sounds/slap.ogg')
challenged = pygame.mixer.Sound('sounds/challenged.ogg')
pile_get = pygame.mixer.Sound('sounds/pile_get.ogg')
com_pile_get = pygame.mixer.Sound('sounds/com_pile_get.ogg')
penalty = pygame.mixer.Sound('sounds/penalty.ogg')
win = pygame.mixer.Sound('sounds/win.ogg')
com_win = pygame.mixer.Sound('sounds/com_win.ogg')

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

class Card: #***[1]***
    def __init__(self, suit=None, value=99, scale=0.5):
        self.suit = suit
        self.value = value
        self.scale = scale
        self.w = int(500*scale)
        self.h = int(726*scale)
        self.rotated = False
        self.set_image()
    def set_image(self):
        if self.value > 10 or self.value <= 1:
            if self.value == 1:
                imgName = 'ace_of_'+self.suit
            elif self.value == 11:
                imgName = 'jack_of_'+self.suit
            elif self.value == 12:
                imgName = 'queen_of_'+self.suit
            elif self.value == 13:
                imgName = 'king_of_'+self.suit
            elif self.value == 14:
                imgName = 'black_rabbit'
            elif self.value == 0:
                imgName = 'white_rabbit'
            else:
                imgName = 'card_back'
                self.w = int(868*self.scale)
                self.h = int(1300*self.scale)
        else:
            imgName = str(self.value)+'_of_'+self.suit
        self.img = pygame.image.load('cards/'+imgName+'.png')
        self.img = pygame.transform.scale(self.img, (self.w,self.h))
    def get_chances(self):
        if self.value == 11:
            return 1
        elif self.value == 12:
            return 2
        elif self.value == 13:
            return 3
        elif self.value == 1:
            return 4
        else:   
            return 13
    def display_card(self, x, y):
        screen.blit(self.img, (x,y))


class Deck: #***[1]***
    def __init__(self):
        self.cards = [Card(suit, value) for value in range(1,14) \
        for suit in ('spades','hearts','diamonds','clubs')]
        self.cards.append(Card('white',0))
        self.cards.append(Card('black',14))
        self.suffle()
    def __len__(self):
        return len(self.cards)
    def suffle(self):
        shuffle(self.cards)
    def push(self, card):
        self.cards.append(card)
    def pop(self):
        return self.cards.pop(0)

    
class Hand: #***[1]***
    def __init__(self):
        self.cards = []
    def __len__(self):
        return len(self.cards)
    def push(self, card):
        self.cards.append(card)
    def pop(self):
        return self.cards.pop(0)
    def align_hand(self):
        for card in self.cards:
            card.set_image()
            card.rotated = False
    def print_hand(self):
        counter = 0
        for card in self.cards:
            counter += 1
            print('(',card.value,'of',card.suit, ')')
        print('card count:',counter)
    
    
class Player: #***[1]***
    def __init__(self, type):
        self.type = type
        self.hand = Hand()
    def play_card(self):
        return self.hand.pop()
    def add_card(self, card):
        self.hand.push(card)
    

class Game: #**[3]**
    def __init__(self, mode):
        self.mode = mode
        self.deck = Deck()
        self.pile = []
        self.p1_turn = True
        self.challenged = False
        self.chances = 1
        #send random event into event queue to trigger computer response
        pygame.time.set_timer(pygame.USEREVENT, 1500)
        self.pre_game()
        self.tutorial()
        self.game_loop()
    def pre_game(self):
        self.p1 = Player('human')
        self.p2 = Player(self.mode)
        while self.deck:
            self.p1.add_card(self.deck.pop())
            self.p2.add_card(self.deck.pop())
    def tutorial(self):
        pygame.mixer.stop()
        white_rabbit = Card('white',0,.25)
        black_rabbit = Card('black',14,.25)
        screen.fill(white)
        self.draw_rule('RULES',30,.5,.05)
        self.draw_rule('GAMEPLAY: Players take turns playing cards in the center pile until a face card or Ace is played.',17,.5,.125)
        self.draw_rule('The other player then has a number of chances to play another face card or Ace. The challenger player',15,.5,.165)
        self.draw_rule('plays their cards, one at a time, until they either draw another face card onto the pile or exhaust all',15,.5,.205)
        self.draw_rule('of their chances. If the challenger player is able to play a face card or Ace, the other player must beat it.',15,.5,.245)
        self.draw_rule('If the initial face card could not be beaten, the player who placed it takes the pile.',15,.5,.285)
        self.draw_rule('CHANCES: four after an Ace, three after a King, two after a Queen, one after a Jack, and 13 after a black rabbit.',15,.5,.34)
        black_rabbit.display_card(width*.82,height*.37)
        self.draw_rule('OBJECTIVE: The player who collects every card in the deck wins the game.',17,.385,.4)
        self.draw_rule('SLAPPING: Certain card combinations, when played, entitle the fastest',17,.37,.46)
        self.draw_rule('player to slap the pile and claim it.',17,.31,.5)
        self.draw_rule('Double Rule: When two cards of equivalent value are laid down consecutively. EX: 5,5',15,.4,.54)
        self.draw_rule('Sandwich Rule: When two cards of equivalent value are laid down consecutively,',15,.383,.58)
        self.draw_rule('but with one card of different value between them. EX: 5,7,5',15,.43,.62)
        self.draw_rule('White Rabbit: Anytime someone lays down a white rabbit, the pile can be slapped.',15,.383,.66)
        white_rabbit.display_card(width*.01,height*.69)
        self.draw_rule('PENALTIES: If players slap the pile when the card combination does not merit',17,.58,.72) 
        self.draw_rule('a slap, the slapper will discard a card face-up at the bottom of the pile.',17,.6,.76)
        self.draw_rule('CONTROLS:',17,.245,.82)
        self.draw_rule('Player 1:',17,.36,.86)
        self.draw_rule('Left Alt: Play Card',17,.44,.9)
        self.draw_rule('Left Ctrl: Slap',17,.419,.94)
        if self.mode == 'human':
            self.draw_rule('Player 2:',17,.59,.86)
            self.draw_rule('Right Alt: Play Card',17,.68,.9)
            self.draw_rule('Right Ctrl: Slap',17,.659,.94)
        self.draw_rule('press any key to continue...',15,.87,.97)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                if event.type == pygame.KEYDOWN:
                    screen.fill(white)
                    return
    def game_loop(self):
        while self.p1.hand and self.p2.hand:
            screen.fill(white)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return 
                    if event.key == pygame.K_h:
                        self.tutorial()
                #sclap controller
                if self.is_legal_slap():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LCTRL:
                            slap.play()
                            while self.pile:  
                                self.p1.add_card(self.pile.pop())
                            self.draw_label('P1 SLAP!',150,.5,.5)
                            self.p1.hand.align_hand()
                            self.p1_turn = True
                            self.challenged = False
                        if event.key == pygame.K_RCTRL:
                            slap.play()
                            while self.pile:
                                self.p2.add_card(self.pile.pop())
                            self.draw_label('P2 SLAP!',150,.5,.5)
                            self.p2.hand.align_hand()
                            self.p1_turn = False
                            self.challenged = False
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LCTRL:
                            self.penalty(self.p1.play_card())
                        if event.key == pygame.K_RCTRL:
                            self.penalty(self.p2.play_card())
                #turn controller
                if self.p1_turn:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LALT:
                            #if the challenge is not beaten, pay out the pile to opponent
                            if self.challenged and self.face.get_chances() < self.chances:
                                    while self.pile:  
                                        self.p2.add_card(self.pile.pop())
                                    self.challenged = False
                                    self.p1_turn = False
                                    self.then = pygame.time.get_ticks()
                                    if self.mode == 'computer':
                                        com_pile_get.play()
                                        self.draw_label('COM WINS THE PILE',30,.5,.5)
                                    else:
                                        pile_get.play()
                                        self.draw_label('P2 WINS THE PILE',30,.5,.5)
                                    self.p2.hand.align_hand()
                            else:
                                #pass the turn if not challenged
                                if not self.challenged:
                                    self.p1_turn = False
                                    self.then = pygame.time.get_ticks()
                                #player 1 play card logic
                                self.card = self.p1.play_card()
                                if self.card.value > 10 or self.card.value == 1:
                                    if self.challenged:
                                        self.p1_turn = False
                                        self.then = pygame.time.get_ticks()
                                    self.face = self.card
                                    self.challenged = True
                                    pygame.mixer.stop()
                                    challenged.play()
                                    self.chances = 1
                                self.pile.append(self.card)
                                if self.challenged and self.p1_turn == True:
                                    self.chances += 1
                else:
                    #computer opponent
                    if self.mode == 'computer':
                        #computer opponent play speed control logic
                        self.now = pygame.time.get_ticks()
                        if self.now - self.then  >= 1000:
                            #if the challenge is not beaten, pay out the pile to opponent
                            if self.challenged and self.face.get_chances() < self.chances:
                                while self.pile:  
                                    self.p1.add_card(self.pile.pop())
                                self.challenged = False
                                self.p1_turn = True
                                pile_get.play()
                                self.draw_label('P1 WINS THE PILE',30,.5,.5)
                                self.p1.hand.align_hand()
                            else:
                                #pass the turn if not challenged
                                if not self.challenged:
                                    self.p1_turn = True
                                #computer play card logic
                                self.card = self.p2.play_card()
                                if self.card.value > 10 or self.card.value == 1:
                                    if self.challenged:
                                        self.p1_turn = True
                                    self.face = self.card
                                    self.challenged = True
                                    pygame.mixer.stop()
                                    challenged.play()
                                    self.chances = 1
                                self.pile.append(self.card)
                                if self.challenged and self.p1_turn == False:
                                    self.chances += 1
                    #human opponent
                    else:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RALT:
                                #if the challenge is not beaten, pay out the pile to opponent
                                if self.challenged and self.face.get_chances() < self.chances:
                                    while self.pile:  
                                        self.p1.add_card(self.pile.pop())
                                    self.challenged = False
                                    self.p1_turn = True
                                    pile_get.play()
                                    self.draw_label('P1 WINS THE PILE',30,.5,.5)
                                    self.p1.hand.align_hand()
                                else:
                                    #pass the turn if not challenged
                                    if not self.challenged:
                                        self.p1_turn = True
                                    #player 2 play card logic
                                    self.card = self.p2.play_card()
                                    if self.card.value > 10 or self.card.value == 1:
                                        if self.challenged:
                                            self.p1_turn = True
                                        self.face = self.card
                                        self.challenged = True
                                        pygame.mixer.stop()
                                        challenged.play()
                                        self.chances = 1
                                    self.pile.append(self.card)
                                    if self.challenged and self.p1_turn == False:
                                        self.chances += 1
            self.draw_title(40,.5,.1)
            self.draw_hands()
            self.draw_pile(275,118)
            pygame.display.update()
            clock.tick(60)
        if self.p1.hand:
            win.play()
            self.draw_label('P1 WIN!',150,.5,.5)
        elif self.p2.hand:
            if self.mode == 'computer':
                com_win.play()
                self.draw_label('COM WIN',150,.5,.5)
            else:
                win.play()
                self.draw_label('P2 WIN!',150,.5,.5) 
        else:
            self.draw_label('loading...',150,.5,.5)
        time.sleep(2)
    def draw_hands(self):
        card = Card('back',99,0.15)
        font = pygame.font.Font('freesansbold.ttf',60)
        #turn highlight
        if self.p1_turn:
            pygame.draw.rect(screen, highlight, (0, height-card.h-5, card.w+5, card.h+5))
        else:
            pygame.draw.rect(screen, highlight, (width-card.w-5, height-card.h-5, card.w+5, card.h+5))
        #draw p1 hand with count
        p1_count = str(len(self.p1.hand))
        card.display_card(0,height-card.h)
        textSurf, textRect = text_objects(p1_count, font)
        textRect.center = (0+(card.w/2),height-(card.h/2))
        screen.blit(textSurf,textRect)
        #drawn p2 hand with count
        p2_count = str(len(self.p2.hand))
        card.display_card(width-card.w,height-card.h)
        textSurf, textRect = text_objects(p2_count, font)
        textRect.center = (width-(card.w/2),height-(card.h/2))
        screen.blit(textSurf,textRect)
    def draw_rule(self,text,size,x_mult,y_mult):
        font = pygame.font.Font('freesansbold.ttf',size)
        textSurf, textRect = text_objects(text, font)
        textRect.center = (width*x_mult,height*y_mult)
        screen.blit(textSurf,textRect)
    def draw_title(self,size,x_mult,y_mult):
        if self.challenged:
            if self.p1_turn:
                text = 'P1 HAS BEEN CHALLENGED'
            elif self.mode == 'computer':
                text = 'COM HAS BEEN CHALLENGED'
            else:
                text = 'P2 HAS BEEN CHALLENGED'
        elif self.p1_turn:
            text = 'P1 TURN'
        elif self.mode == 'computer':
            text = 'COM TURN'
        else:
            text = 'P2 TURN'
        font = pygame.font.Font('freesansbold.ttf',size)
        textSurf, textRect = text_objects(text, font)
        textRect.center = (width*x_mult,height*y_mult)
        screen.blit(textSurf,textRect)
    def draw_label(self,text,size,x_mult,y_mult):
        screen.fill(white)
        font = pygame.font.Font('freesansbold.ttf',size)
        textSurf, textRect = text_objects(text, font)
        textRect.center = (width*x_mult,height*y_mult)
        screen.blit(textSurf,textRect)
        pygame.display.update()
        time.sleep(1)
    def draw_pile(self,x,y):
        if self.pile:
            angle = 0
            for card in self.pile:
                if card.rotated == False:
                    card.img = pygame.transform.rotate(card.img, angle*-1)
                    card.rotated = True
                if angle == 0:
                    card.display_card(x,y)
                elif angle == 45 or angle == 135:
                    card.display_card(x-90,y-20)
                else:
                    card.display_card(x-56,y+56)
                angle = (angle+45)%180
    def print_pile(self):
        for card in self.pile:
            print('(',card.value,'of',card.suit, ')')
    def is_legal_slap(self):
        if len(self.pile) > 1 and self.pile[len(self.pile)-1].value == self.pile[len(self.pile)-2].value:
            return True
        elif len(self.pile) > 2 and self.pile[len(self.pile)-1].value == self.pile[len(self.pile)-3].value:
            return True
        else:
            for card in self.pile:
                if card.value == 0:
                    return True
        return False
    def penalty(self, discard):
        pygame.mixer.stop()
        penalty.play()
        self.pile.insert(0,discard)
        for card in self.pile:
            card.set_image()
            card.rotated = False
        


class Menu: #***[2]***
    def __init__(self):
        self.menu = True
        self.deck = Deck()
        pygame.mixer.music.play(-1)
        self.draw_menu()
    def draw_menu(self):
        while self.menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            #mouse detection variables
            self.mouse = pygame.mouse.get_pos()
            self.click = pygame.mouse.get_pressed()
            #draw cards on screen (scroll over to slow rotation)
            screen.fill(white)
            self.draw_cards(275,118)
            #draw game name
            self.draw_label('RATSLAP',115,.5,.1)
            #draw button boxes with functionality
            self.draw_button('vs player', 134, 490, 200, 90, 'human')
            self.draw_button('vs computer', 470, 490, 200, 90, 'computer')
            #update screen/fps
            pygame.display.update()
            clock.tick(60)
    def draw_cards(self,x,y):
        card = self.deck.pop()
        card.display_card(x,y)
        self.deck.push(card)
        if x+card.w > self.mouse[0] > x and y+card.h > self.mouse[1] > y:
            time.sleep(1)
    def draw_button(self,text,x,y,w,h,action=None):
        #draw rectangles
        pygame.draw.rect(screen, black, (x, y, w, h))
        pygame.draw.rect(screen, white, (x+2, y+2, w-4, h-4))
        #draw button text
        font = pygame.font.Font('freesansbold.ttf',20)
        textSurf, textRect = text_objects(text, font)
        textRect.center = (x+(w/2),y+(h/2))
        screen.blit(textSurf,textRect)
        #button functionality (start game with loading screen)
        if x+w > self.mouse[0] > x and y+h > self.mouse[1] > y:
            pygame.draw.rect(screen, black, (textRect[0], textRect[1]+textRect[3], textRect[2], 2))
            if self.click[0] == 1 and action != None:
                pygame.mixer.music.stop()
                screen.fill(white)
                self.draw_label('loading...',115,.5,.5)
                pygame.display.update()
                shuffling.play()
                Game(action)
                pygame.mixer.music.play(-1)
                print('GAME OVER')
    def draw_label(self,text,size,x_mult,y_mult):
        font = pygame.font.Font('freesansbold.ttf',size)
        textSurf, textRect = text_objects(text, font)
        textRect.center = (width*x_mult,height*y_mult)
        screen.blit(textSurf,textRect)


def main(): #***[1]***
    Menu()


if __name__ == "__main__": #***[1]***
    main()