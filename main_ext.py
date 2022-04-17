import random

class Card:
    def __init__(self, value, suit):
        self.__value = value
        self.__suit = suit
    
    #Creates string representation of Card instance to write to output. 
    def __str__(self):
        return str(self.__value) + str(self.__suit)
    
    #Rewrite the = operator to check if both value and suit match for two instances of Card. 
    def __eq__(self, other):
        if self.__value == other.__value and self.__suit == other.__suit:
            return True
        else:
            return False
    
    #Rewrite the + operator so that for instances of Card, Card + 1 gives the next sequential card, preserving suit, so that the game can check that the cards are in order. 
    def __add__(self, other):
        if type(other) == int:
            return Card(self.__value + other, self.__suit)
        elif type(self) == int:
            return Card(other.__value + self, other.__suit)
        else:
            raise ValueError("Custom card additon failed")
    
class CardPile:
    def __init__(self):
        self.__items = []

    def get_items(self):
        return self.__items

    def add_top(self, item):
        self.__items = [item] + self.__items
    def add_bottom(self, item):
        self.__items = self.__items + [item]

    #Remove and return bottom/top item from stack.
    def remove_top(self):
        top_item = self.__items[0]
        self.__items = self.__items[1:]
        return top_item
    def remove_bottom(self):
        bottom_item = self.__items[-1]
        self.__items = self.__items[:-1]
        return bottom_item
    
    def size(self):
        return len(self.__items)
    
    #Remove without returning bottom/top item from stack. 
    def peek_top(self):
        return self.__items[0]
    def peek_bottom(self):
        return self.__items[-1]
    
    #String representation of stack for display during gameplay.
    def print_all(self, index):
        if index == 0:
            string = ""                 #defining string here avoids throwing an error when the pile is empty
            if len(self.__items) > 0:   #the error would be thrown here, an empty pile does not pass this condition if the string is never assigned. 
                string = str(self.__items[0]) + " *"*(len(self.__items)-1)
            print(string)
        else:
            string = ""                 
            for item in self.__items:
                string += str(item) + " "
            string.strip()
            print(string)
    
    def shuffle(self):
        return random.shuffle(self.__items)

class Solitaire:
    def __init__(self, cards=[]):
        #Settings() creates instance of Settings class which handles read/write of settings.txt
        self.__settings = Settings()
        self.__full_settings_list = self.__settings.get_full_list()      #imports list of settings for assignment

        #Assigns settings tthat werte imported above by Settings class.  
        self.select_difficulty()
        self.__range = (1, self.__settings[1])
        self.__max_num_moves = self.__settings[2]
        suits_string = self.__settings[4]
        self.__num_suits = self.__settings[3]
        self.__suits = suits_string[:self.__settings[3]]

        self.__num_piles = (self.__range[1]//8) + 3 + len(self.__suits)     #Pile number generator outlined in assignment specifications. 
        
        #Generator for piles, which are instances of CardPile, as well as generator for Card instances in each pile. 
        self.__piles = []
        for i in range(self.__num_piles):
            self.__piles.append(CardPile())
        for suit in self.__suits:
            for value in range(self.__range[0], self.__range[1] + 1):
                self.__piles[0].add_bottom(Card(value, suit))

        self.__piles[0].shuffle()

    def get_pile(self, i):
        return self.__piles[i]
    
    def display(self):
        for index in range(self.__num_piles):
            print("{}:".format(index), end=" ")
            self.__piles[index].print_all(index)
    
    #defining the move method which determines if a move is legal, then pops/pushes between stacks to move the Card instances. 
    def move(self, p1, p2):
        #Player can spend one move to move top card to bottom of stack (also hides the moved card).
        if p1 == p2 == 0:
            draw_pile = self.get_pile(0)
            if draw_pile.size() > 0:
                top = draw_pile.remove_top()
                draw_pile.add_bottom(top)

        #Player can move from draw pile which reveals the next card. 
        elif p1 == 0 and p2 > 0:
            draw_pile = self.get_pile(0)
            p2_pile = self.get_pile(p2)
            if draw_pile.size() > 0:
                if p2_pile.size() > 0:
                    if p2_pile.peek_bottom() == draw_pile.peek_top() + 1:
                        top_draw_pile = draw_pile.remove_top()
                        p2_pile.add_bottom(top_draw_pile)
                else:
                    top_p1 = draw_pile.remove_top()
                    p2_pile.add_bottom(top_p1)
        
        #Player can move between two non-draw piles.
        elif p1 > 0 and p2 > 0:
            start_pile = self.get_pile(p1)
            final_pile = self.get_pile(p2)
            if start_pile.size() > 0 and final_pile.size() > 0:
                if final_pile.peek_bottom() == start_pile.peek_top() + 1:
                    while start_pile.size() > 0:
                        top_p1 = start_pile.remove_top()
                        final_pile.add_bottom(top_p1)
        else:
            print("Illegal move! Try again.")

    def is_complete(self):
        #Win condition 1: empty starting pile
        draw_pile_is_empty = False
        draw_pile = self.get_pile(0)
        if draw_pile.size() == 0:
            draw_pile_is_empty = True
        
        #Win condition 2: all cards on a number of piles equal to the number of suits
        full_piles = False
        pile_sizes = [self.get_pile(i).size() for i in range(self.__num_piles)]
        num_nonzeroes = 0
        nonzero_indices = [] 
        for i in range(len(pile_sizes)):
            if pile_sizes[i] > 0:
                num_nonzeroes += 1
                nonzero_indices.append(i)
        if num_nonzeroes == self.__num_suits:
            full_piles = True

        #Win condition 3 (descending order) is guaranteed by there being full stacks, as the cards can't be added to the stack out of order. 

        #Final check
        if full_piles == True and draw_pile_is_empty == True:
            return True
        else:
            return False
    
    #Method to fetch and validate move input from user. Uses while loops to fetch data from user until valid input is given. 
    def get_move_input(self, move_number):
        print("Round", move_number, "out of", self.__max_num_moves, end = ": ")
        row1 = None
        while row1 == None:
            try:
                row1_temp = int(input("Move from row no.:"),10)    #placeholder for row1 while determining validity
                if row1_temp > self.__num_piles-1 or row1_temp < 0:
                    raise ValueError
                else:
                    row1 = row1_temp                 #confirm assignment of row1
            except:
                print("Error! Please enter a valid row number (an integer!)")
                print("Round", move_number, "out of", self.__max_num_moves, end = ": ")
        

        print("Round", move_number, "out of", self.__max_num_moves, end = ": ")
        row2 = None
        while row2 == None:
            try:
                row2_temp = int(input("Move to row no.:"),10)    #placeholder for row2 while determining validity
                if row2_temp > self.__num_piles-1 or row2_temp < 0:
                    raise ValueError
                else:
                    row2 = row2_temp                 #confirm assignment of row2
            except:
                print("Error! Please enter a valid row number (an integer!)")
                print("Round", move_number, "out of", self.__max_num_moves, end = ": ")

        return row1, row2

    
    def select_difficulty(self):
        full_settings_list = self.__settings.get_full_list()
        change_settings_bool = input("Your current difficulty is: {}. Would you like to change difficulties? (y/n)".format(self.__settings[0]))
        accepted_inputs = ["y", "n"]
        while change_settings_bool not in accepted_inputs:
            print("Invalid input! Try again.")
            change_settings_bool = input("Your current difficulty is: {}. Would you like to change difficulties? (y/n)".format(self.__settings[0]))
        
        while change_settings_bool != "n":
            string = ""
            string += "Enter the number corresponding to your desired difficulty:" + "\n"
            for index in range(1, len(full_settings_list)):
                string += "{}: {}\n".format(index, full_settings_list[index][0])
            
            #the following block is the same structure as the above one for change_settings_bool
            difficulty = input(string)
            accepted_inputs = [str(x) for x in range(1, len(full_settings_list))]
            while difficulty not in accepted_inputs:
                print("Invalid input! Try again.")
                difficulty = input(string)
            difficulty = int(difficulty)

            self.__settings.change_difficulty(difficulty)

            change_settings_bool = input("Your current difficulty is: {}. Would you like to change difficulties? (y/n)".format(self.__settings[0]))
            accepted_inputs = ["y", "n"]
            while change_settings_bool not in accepted_inputs:
                print("Invalid input! Try again.")
                change_settings_bool = input("Your current difficulty is: {}. Would you like to change difficulties? (y/n)".format(self.__settings[0]))
        
        self.__edited_settings = False
        if self.__settings[0] == "Custom":
            self.__edited_settings = True
            self.change_custom_settings()

    def change_custom_settings(self):
        text = "Your current Custom difficulty settings are:" + "\n"
        text += self.__settings.convert_data_list_to_string() + "\n"
        text += "\n"
        text += "Enter a number to edit these settings." + "\n"
        text += "1: Change Range" + "\n"
        text += "2: Change Moves" + "\n"
        text += "3: Change Number of Suits" + "\n"
        text += "4: Change Default Suits" + "\n"
        text += "5: Play" + "\n"
        change_custom_settings_input = input(text)
        accepted_inputs = [str(x) for x in range(1, 6)]
        while change_custom_settings_input not in accepted_inputs:
            print("Invalid input! Try again.")
            change_custom_settings_input = input(text)
        
        if change_custom_settings_input == "1":
            finished = False
            while finished == False:
                rang = input("Please enter the largest number in the deck: ")
                try:
                    rang = int(rang)
                    finished = True
                except:
                    print("Invalid input! Try again")
            
            self.__settings[1] = rang
        
        if change_custom_settings_input == "2":
            finished = False
            while finished == False:
                moves = input("Please enter the maximum number of moves: ")
                try:
                    moves = int(moves)
                    finished = True
                except:
                    print("Invalid input! Try again")
            
            self.__settings[2] = moves
        
        if change_custom_settings_input == "3":
            finished = False
            while finished == False:
                num_suits = input("Please enter the desired number of suits: ")
                try:
                    num_suits = int(num_suits)
                    finished = True
                except:
                    print("Invalid input! Try again")
            
            self.__settings[3] = num_suits
        
        if change_custom_settings_input == "4" or self.__settings[3] > len(self.__settings[4]):
            suits = []

            while len(suits)< self.__settings[3]:
                new_suit = input("Please enter a symbol for a suit: ")
                suits.append(new_suit)
            
            self.__settings[4] = suits
        
        if change_custom_settings_input == "5":
            return None

    def play(self):
        if self.__edited_settings == True:
            self.__settings.write_settings_file()

            self.__range = (1, self.__settings[1])
            self.__max_num_moves = self.__settings[2]
            suits_string = self.__settings[4]
            self.__num_suits = self.__settings[3]
            self.__suits = suits_string[:self.__settings[3]]

            self.__num_piles = (self.__range[1]//8) + 3 + len(self.__suits)
        
            self.__piles = []
            for i in range(self.__num_piles):
                self.__piles.append(CardPile())
            for suit in self.__suits:
                for value in range(self.__range[0], self.__range[1] + 1):
                    self.__piles[0].add_bottom(Card(value, suit))

            self.__piles[0].shuffle()
        print("********************** NEW GAME *****************************")
        move_number = 1
        while move_number <= self.__max_num_moves and not self.is_complete():
            self.display()
            
            row1, row2 = self.get_move_input(move_number)

            self.move(row1, row2)
            move_number += 1
            
        if self.is_complete():
            print("You Win in", move_number - 1, "steps!\n")
        else:
            print("You Lose!\n")

class Settings:
    def __init__(self):
        self.__settings_list = interpret_settings_file()
        for difficulty_settings in self.__settings_list[1:]:
                if difficulty_settings[0] == self.__settings_list[0][0]:
                    current_settings = difficulty_settings
        self.__current_settings = current_settings
    
    def __getitem__(self, index):
        return self.__current_settings[index]
    def __setitem__(self, index, data):
        self.__current_settings[index] = data
    
    def get_full_list(self):
        return self.__settings_list
    
    def convert_data_list_to_string(self, settings_data=None):
        if settings_data == None:
            settings_data = self.__current_settings

        string = ""
        string += str(settings_data[0]) + "\n"
        string += "Range: " + str(settings_data[1]) + "\n"
        string += "Moves: " + str(settings_data[2]) + "\n"
        string += "Number of Suits: " + str(settings_data[3]) + "\n"
        suits_string = ""
        for suit in settings_data[4]:
            suits_string += suit + " "
        suits_string = suits_string.strip()
        string += "Default Suits: " + suits_string
        
        return string
    
    def change_difficulty(self, difficulty_index):
        difficulty_index -= 1
        difficulty_list = []
        for index in range(1, len(self.__settings_list)):
            difficulty_list.append(self.__settings_list[index][0])
        
        difficulty = difficulty_list[difficulty_index]
        self.__settings_list[0] = [difficulty]

        for presets in self.__settings_list[1:]:
                if presets[0] == difficulty:
                    current_settings = presets
        self.__current_settings = current_settings

        self.write_settings_file()

    def write_settings_file(self):
        string_to_write = "#####" + "\n"
        string_to_write += str(self.__current_settings[0]) + "\n"
        string_to_write += "#####" + "\n"
        for setting in self.__settings_list[1:]:
            string_to_write += self.convert_data_list_to_string(setting) + "\n"
            string_to_write += "#####" + "\n"
        
        string_to_write = string_to_write[:-6] #removes the extra ####


        file = open("settings.txt", "w")
        file.write(string_to_write)
        file.close()
        return string_to_write
    
def interpret_settings_file():
    filename = "settings.txt"
    with open(filename, "r") as file:
        text = file.read()
        
    upper_list = text.split("#####")
 
    for index in range(len(upper_list)):
        upper_list[index] = upper_list[index].split("\n")
    upper_list.pop(0)
    
    for sub_list in upper_list:
        sub_list.pop(0)
        sub_list.pop(-1)

    final_upper_list = []
    for sub_list in upper_list:
        final_lower_list = [sub_list[0]]
        for index in range(1, len(sub_list)):  
            starting_index = sub_list[index].index(":") + 2
            try:
                final_lower_list.append(int(sub_list[index][starting_index:]))
            except ValueError:
                final_lower_list.append(sub_list[index][starting_index:].split())
        final_upper_list.append(final_lower_list)

    return(final_upper_list)

game = Solitaire()
game.play()
