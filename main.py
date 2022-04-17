#Ass.py submission by Jared Andre Rabie, 
#UPI: jrab495,
#Student ID: 728 359 579.

class CardPile:
    def __init__(self):
        self.__items = []

    def get_items(self):
        return self.__items

    def add_top(self, item):
        self.__items = [item] + self.__items
    def add_bottom(self, item):
        self.__items = self.__items + [item]

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
    def peek_top(self):
        return self.__items[0]
    def peek_bottom(self):
        return self.__items[-1]
    
    def print_all(self, index):
        if index == 0:
            string = ""                 #defining string here avoids throwing an error when the pile is empty
            if len(self.__items) > 0:   #the error would be thrown here, an empty pile does not pass this condition the string is never assigned. 
                string = str(self.__items[0]) + " *"*(len(self.__items)-1)
            print(string)
        else:
            string = ""                 #defining string here avoids throwing an error when the pile is empty
            for item in self.__items:
                string += str(item) + " "
            string.strip()
            print(string)

class Solitaire:
    def __init__(self, cards):
        self.__num_cards = len(cards)
        self.__num_piles = (self.__num_cards // 8) + 3
        self.__max_num_moves = self.__num_cards * 2

        self.__piles = []
        for i in range(self.__num_piles):
            self.__piles.append(CardPile())
        for i in range(self.__num_cards):
            self.__piles[0].add_bottom(cards[i])

    def get_pile(self, i):
        return self.__piles[i]
    
    def display(self):
        for index in range(self.__num_piles):
            print("{}:".format(index), end=" ")
            self.__piles[index].print_all(index)
                
    def move(self, p1, p2):
        if p1 == p2 == 0:
            draw_pile = self.get_pile(0)
            if draw_pile.size() > 0:
                top = draw_pile.remove_top()
                draw_pile.add_bottom(top)

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

        elif p1 > 0 and p2 > 0:
            start_pile = self.get_pile(p1)
            final_pile = self.get_pile(p2)
            if start_pile.size() > 0 and final_pile.size() > 0:
                if final_pile.peek_bottom() == start_pile.peek_top() + 1:
                    
                    while start_pile.size() > 0:
                        top_p1 = start_pile.remove_top()
                        final_pile.add_bottom(top_p1)

    def is_complete(self):
        #condition 1: empty starting pile
        draw_pile_is_empty = False
        draw_pile = self.get_pile(0)
        if draw_pile.size() == 0:
            draw_pile_is_empty = True
        
        #condition 2: all cards on one pile
        one_pile = False
        pile_sizes = [self.get_pile(i).size() for i in range(self.__num_piles)]
        num_nonzeroes = 0
        nonzero_index = self.__num_piles + 1 
        for i in range(len(pile_sizes)):
            if pile_sizes[i] > 0:
                num_nonzeroes += 1
                nonempty_pile_index = i
        if num_nonzeroes == 1:
            one_pile = True
        
        #condition 3: all cards descending order
        if draw_pile_is_empty == True and one_pile == True:
            cards = self.get_pile(nonempty_pile_index).get_items()
            descending_order = False
            if cards[::-1] == sorted(cards):
                descending_order = True
        
        #final check
        if one_pile == True and draw_pile_is_empty == True and descending_order == True:
            return True
        else:
            return False
 
    def play(self):
        print("********************** NEW GAME *****************************")
        move_number = 1
        while move_number <= self.__max_num_moves and not self.is_complete():
            self.display()
            print("Round", move_number, "out of", self.__max_num_moves, end = ": ")
            row1 = int(input("Move from row no.:"),10)
            print("Round", move_number, "out of", self.__max_num_moves, end = ": ")
            row2 = int(input("Move to row no.:"),10)
            if row1 >= 0 and row2 >= 0 and row1 < self.__num_piles and row2 < self.__num_piles:
                self.move(row1, row2)
            move_number += 1
            
        if self.is_complete():
            print("You Win in", move_number - 1, "steps!\n")
        else:
            print("You Lose!\n")


