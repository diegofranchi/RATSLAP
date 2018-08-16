-----
Title
-----

    RATSLAP v1.4.20
    CPSC 386 - Into to Game Design and Production
    Project 2: Simple Classic Video Game in Python
    Professor C.Siska - California State University, Fullerton
    April 2, 2018

------------
Contact Info
------------ 

    Diego Franchi
    CWID: 889894283
    email: diegofranchi@csu.fullerton.edu

----------
Files List
---------- 

    cards/
        2_of_clubs.png
        2_of_diamonds.png
        2_of_hearts.png
        2_of_spades.png
        3_of_clubs.png
        3_of_diamonds.png
        3_of_hearts.png
        3_of_spades.png
        4_of_clubs.png
        4_of_diamonds.png
        4_of_hearts.png
        4_of_spades.png
        5_of_clubs.png
        5_of_diamonds.png
        5_of_hearts.png
        5_of_spades.png
        6_of_clubs.png
        6_of_diamonds.png
        6_of_hearts.png
        6_of_spades.png
        7_of_clubs.png
        7_of_diamonds.png
        7_of_hearts.png
        7_of_spades.png
        8_of_clubs.png
        8_of_diamonds.png
        8_of_hearts.png
        8_of_spades.png
        9_of_clubs.png
        9_of_diamonds.png
        9_of_hearts.png
        9_of_spades.png
        10_of_clubs.png
        10_of_diamonds.png
        10_of_hearts.png
        10_of_spades.png
        ace_of_clubs.png
        ace_of_diamonds.png
        ace_of_hearts.png
        ace_of_spades.png
        black_rabbit.png
        card_back.png
        jack_of_clubs.png
        jack_of_diamonds.png
        jack_of_hearts.png
        jack_of_spades.png
        king_of_clubs.png
        king_of_diamonds.png
        king_of_hearts.png
        king_of_spades.png
        queen_of_clubs.png
        queen_of_diamonds.png
        queen_of_hearts.png
        queen_of_spades.png
        white_rabbit.png
    sounds/
        challenged.ogg
        com_pile_get.ogg
        com_win.ogg
        menu_song.ogg
        penalty.ogg
        pile_get.ogg
        shuffling.ogg
        slap.ogg
        win.ogg
    ratscrew.py
    README.txt

---------------------
Installation/Run Info
---------------------

    Example: python ratscrew.py
    
    Required: 
        Python 2.7 or Python 3.6 Downloaded
        pygame library installed

----------
Game Rules
----------

    GAMEPLAY: Players take turns playing cards in the center pile until a face card or Ace is played.
              The other player then has a number of chances to play another face card or Ace. The challenger player
              plays their cards, one at a time, until they either draw another face card onto the pile or exhaust all
              of their chances. If the challenger player is able to play a face card or Ace, the other player must beat it.
              If the initial face card could not be beaten, the player who placed it takes the pile.
        
    CHANCES: four after an Ace, three after a King, two after a Queen, one after a Jack, and 13 after a black rabbit.
    
    OBJECTIVE: The player who collects every card in the deck wins the game.
    
    SLAPPING: Certain card combinations, when played, entitle the fastest
              player to slap the pile and claim it.
      Double Rule: When two cards of equivalent value are laid down consecutively. EX: 5,5
      Sandwich Rule: When two cards of equivalent value are laid down consecutively,
                     but with one card of different value between them. EX: 5,7,5
      White Rabbit: Anytime someone lays down a white rabbit, the pile can be slapped.
    
    PENALTIES: If players slap the pile when the card combination does not merit
               a slap, the slapper will discard a card face-up at the bottom of the pile.
    CONTROLS:
        Player 1:
            Left Alt: Play Card
            Left Ctrl: Slap
        Player 2:
            Right Alt: Play Card
            Right Ctrl: Slap
        During Game:
            h: help menu

-------------- 
Bugs Remaining 
--------------

    The game ends when no cards remain in a players hand (as it should), but
    this game does not take into account if the last card played is a face card.
    (the game would continue until the challenged player beats the last card
     or the game would continue with the challenger winning the pile)
     
    Otherwise no bugs

--------------
Features Added
--------------

    White Rabbit: Anytime someone lays down a white rabbit, the pile can be slapped.
    Black Rabbit: Face Card (starts challenge) with 13 chances to beat it

    Main menu song loop
    Cards on the menu screen stop then slowly revolve when moused over
    Menu buttons underline when moused over
    Deck suffling loading sound
    Decks are highlighted yellow during your turn in game
    Cards in game will always appear in the center in one of 4 angles (0,45,90,135)
    Slap sound fx
    Penalty sound fx
    Challenge win sound fx
    Win fanfare
    Unique computer opponent win sounds
    
    



