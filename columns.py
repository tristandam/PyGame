#Tristan Dam 12129189
# columns.py


# add more unit tests

class Faller:
    def __init__(self, contents:list, column:int) -> None:
        "Initializes a faller with its contents and column to drop in"
        self.contents = contents
        self.column = column
        self.count = 0
        self.active = True
        self.freeze = False
        self.should_rotate = False
        self.move_left = False
        self.move_right = False
    def rotate_faller_contents(self):
        self.contents = [self.contents[2],self.contents[0],self.contents[1]]
    


class Gamestate:
    def __init__(self,rows:int,columns:int):
        self.board = self.create_empty_board(rows,columns)
        self.game_active = True
    def create_empty_board(self, rows:int, columns:int):
        'Create a two dimensional list of the given number of rows and columns)'
        board = []
        for row in range(rows):
            board.append([0]*columns)
        return board
    def create_specific_board(self, contents:[[list]])->None:
        'Given desired contents, create a board with those contents'
        self.board = contents
    def mutate_board(self, list_of_contents:list)-> None:
        'Given a board and the desired contents, changes the contents of the board'
        for row in range(len(self.board)):
            self.board[row] = list_of_contents[row]
    def drop_jewels(self)-> None:
        'Takes a board, and drops every piece that has an empty space below it'
        for count in self.board: # do this the amount of rows the board has
            for row in reversed(range(len(self.board))): # starting from the bottom:
                if row != 0:  # if we're not at the top row in the board:
                        for element in range(len(self.board[row])):
                                if self.board[row][element] == 0: #if the piece is 0:
                                        self.board[row][element] = self.board[row-1][element] #the piece above the hole falls down
                                        self.board[row-1][element] = 0                   #the piece that fell is now becomes empty
                    

    def print_board(self)->None:
        'Given a 2dlist/board, prints out the board in correct format'
        number_of_dashes = 3*len(self.board[0])
        for row in self.board:
            print('|',end = "")
            for element in row:
                if element == 0:
                    print('   ',end="")
                elif str(element) in 'STVWXYZ':
                    print(' {} '.format(element),end="")
                else:
                    print('{}'.format(element),end="")
            print('|')
        print(' {} '.format('-'*number_of_dashes))

    
    def check_for_freezing(self,faller:Faller)->None:
        'Given the current state of the faller, looks below to see if it should prepare to freeze as | |'
        try:
             if self.board[faller.count+1][faller.column] != 0:
                self.faller_prepares_to_freeze(faller)
        except IndexError:
            self.faller_prepares_to_freeze(faller)
        

    def faller_prepares_to_freeze(self,faller:Faller)->None:
        "Given a faller's attributes, change the brackets to lines in the board"
        try:
            self.board[faller.count][faller.column] = self.board[faller.count][faller.column].replace("[","|").replace("]","|")
            self.board[faller.count-1][faller.column] = self.board[faller.count-1][faller.column].replace("[","|").replace("]","|")
            self.board[faller.count-2][faller.column] = self.board[faller.count-2][faller.column].replace("[","|").replace("]","|")
            faller.freeze = True 
        except IndexError:
            pass
        finally:
            faller.freeze = True

    def faller_freezes(self,faller:Faller)->None:
        "This function is used to turn fallers that are prepared to freeze to actually freeze. Then they can no longer be worked with."
        faller.count -= 1
        self.board[faller.count-2][faller.column] = self.board[faller.count-2][faller.column].replace("|","")
        self.board[faller.count-1][faller.column] = self.board[faller.count-1][faller.column].replace("|","")
        self.board[faller.count][faller.column] = self.board[faller.count][faller.column].replace("|","")
        self.print_board()
        faller.active = False
        for jewel in self.board[0]:
            if jewel != 0:
                self.game_active = False
                print("GAME OVER")


    def faller_moves_left(self,faller:Faller)->None:
        "Moves a jewel left, and prints the board."
        self.print_board()
        faller.move_left = False
        


    def faller_moves_right(self,faller:Faller)->None:
        "Moves a jewel right, and prints the board."
        self.print_board()
        faller.move_right = False

    def reset_faller(self,faller)->None:
        "Set the faller's should rotate attribute to false, and print the board."
        self.print_board()
        faller.should_rotate = False


    def move_left_1(faller:Faller)->None:
        'Moves the faller left on 1st faller iteration'
        try:
            if self.board[faller.count][faller.column-1] == 0 and faller.column != 0:
                self.board[faller.count][faller.column-1] = '[{}]'.format(str(faller.contents[-1]))
                self.board[faller.count][faller.column] = 0
                self.check_for_freezing(faller)
                self.faller_moves_left(faller)
                faller.column -=1
            else:
                self.faller_moves_left(faller)
        except IndexError:
                self.faller_moves_left(faller)
    def move_right_1(faller:Faller)->None:
        'Moves the faller right on 1st faller iteration'
        try:
            if self.board[faller.count][faller.column+1] == 0:
                self.board[faller.count][faller.column+1] = '[{}]'.format(str(faller.contents[-1]))
                self.board[faller.count][faller.column] = 0
                self.check_for_freezing(faller)
                self.faller_moves_right(faller)
                faller.column +=1
            else:
                self.faller_moves_right(faller)
        except IndexError:
                self.faller_moves_right(faller) 

    def bottom_faller_jewel(self,faller:Faller) -> None:
        '''Places the initial bottom jewel at the top of the board. If anything else needs to be moved, this
        function handles that as well.'''
        if faller.should_rotate:
            faller.rotate_faller_contents()
            self.board[faller.count][faller.column] = '[{}]'.format(str(faller.contents[-1]))
            self.check_for_freezing(faller)
            self.reset_faller(faller)
        elif faller.move_left:
            self.move_left_1(faller)
        elif faller.move_right:
            self.move_right_1(faller)        
        else:
            self.board[faller.count][faller.column] = '[{}]'.format(str(faller.contents[-1]))
            self.check_for_freezing(faller)
            self.print_board()
            faller.count+=1
        
    
    def move_left_2(self,faller:Faller) -> None:
        'Moves the faller left on the second faller iteration.'
        try:
            if self.board[faller.count-1][faller.column-1] == 0 and faller.column != 0:
                if self.board[faller.count-1][faller.column-1] == 0:
                        faller.freeze = False
                        self.board[faller.count-1][faller.column] = 0
                        self.board[faller.count-1][faller.column-1] = '[{}]'.format(str(faller.contents[-1]))
                        self.faller_moves_left(faller)
                        faller.column-=1                
                else:
                    faller.freeze = True    
                    self.board[faller.count-1][faller.column] = 0
                    self.board[faller.count-1][faller.column-1] = '|{}|'.format(str(faller.contents[-1]))
                    self.faller_moves_left(faller)
                    faller.column-=1
            else:
                self.faller_moves_left(faller)        
        except IndexError:
            self.faller_moves_left(faller)

    def move_right_2(self,faller:Faller) ->None:
        'Moves the faller right on the second faller iteration.'
        try: 
            if self.board[faller.count-1][faller.column+1] == 0:
                if self.board[faller.count-2][faller.column+1] == 0:
                        faller.freeze = False
                        self.board[faller.count-1][faller.column] = 0
                        self.board[faller.count-1][faller.column+1] = '[{}]'.format(str(faller.contents[-1]))
            
                else:
                    faller.freeze = True
                    self.board[faller.count-1][faller.column] = 0
                    self.board[faller.count-1][faller.column+1] = '|{}|'.format(str(faller.contents[-1]))
                self.faller_moves_right(faller)
                faller.column +=1
            else:
                self.faller_moves_right(faller)
        except IndexError:
            self.faller_moves_right(faller)


    def bottom_2_faller_jewels(self,faller:Faller) -> None:
        'Based on what faller attribute is active, perform said attribute on the faller'
        if faller.should_rotate:
             faller.rotate_faller_contents()
             self.board[faller.count-1][faller.column] = '[{}]'.format(str(faller.contents[-1])) 
             self.reset_faller(faller)
        elif faller.move_left:
            self.move_left_2(faller)
        elif faller.move_right:
            self.move_right_2(faller)
        else:
             self.board[faller.count-1][faller.column] = '[{}]'.format(str(faller.contents[-2])) 
             self.board[faller.count][faller.column] = '[{}]'.format(str(faller.contents[-1])) 
             self.check_for_freezing(faller)
             self.print_board()
             faller.count+=1
           
      

    def check_left_2_empty(self,faller:Faller):
        'Checks if the left 2 spaces on the board are available to move to'
        return (self.board[faller.count-2][faller.column-1] == 0 and
                self.board[faller.count-1][faller.column-1] == 0 and
                faller.column!= 0)

    def check_right_2_empty(self,faller:Faller):
        'Checks if the right 2 spaces on the board are available to move to'
        try:
            return (self.board[faller.count-2][faller.column+1] == 0 and
                    self.board[faller.count-1][faller.column+1] == 0)
        except IndexError:
            pass


    def update_2_jewels(self,faller:Faller,str1:str,str2:str,shift=int):
        'Given 2 slots on the board, replace contents with given strings.'
        self.board[faller.count-2][faller.column+shift] = (str1+'{}'+str2).format(str(faller.contents[-2]))
        self.board[faller.count-1][faller.column+shift] = (str1+'{}'+str2).format(str(faller.contents[-1]))

    def move_left_3(self,faller:Faller):
        'Moves the faller left on the third faller iteration.'
        if self.check_left_2_empty(faller):
           if self.board[faller.count][faller.column-1] == 0:
               faller.freeze = False  
               self.update_2_jewels(faller,'[',']',-1)
           else:
                faller.freeze = True
                self.update_2_jewels(faller,'|','|',-1)
           self.board[faller.count-2][faller.column] = 0
           self.board[faller.count-1][faller.column] = 0
           self.faller_moves_left(faller)
           faller.column-=1
        else:
            self.faller_moves_left(faller)

    def move_right_3(self,faller:Faller):
        'Moves the faller right on the third faller iteration.'
        if self.check_right_2_empty(faller):
           if self.board[faller.count][faller.column+1] == 0:
               faller.freeze = False
               self.update_2_jewels(faller,'[',']',+1)
           else:
                faller.freeze = True
                self.update_2_jewels(faller,'|','|',+1)
           self.board[faller.count-2][faller.column] = 0
           self.board[faller.count-1][faller.column] = 0
           self.faller_moves_right(faller)
           faller.column+=1
        else:
           self.faller_moves_right(faller)

    def bottom_3_faller_jewels(self,faller:Faller) -> None:
        'Based on the faller attribute for the third faller iteration, perform said action (such as rotate, move left, etc.)'
        if faller.should_rotate:
              faller.rotate_faller_contents()
              self.update_2_jewels(faller,'[',']',0)
              self.reset_faller(faller)
        elif faller.move_left:
               self.move_left_3(faller)
        elif faller.move_right:
               self.move_right_3(faller)
        else:
            self.board[faller.count-2][faller.column] = '[{}]'.format(str(faller.contents[-3]))
            self.board[faller.count-1][faller.column] = '[{}]'.format(str(faller.contents[-2]))
            self.board[faller.count][faller.column] = '[{}]'.format(str(faller.contents[-1]))
            self.check_for_freezing(faller)
            self.print_board()
            faller.count+=1
          



    def check_left_3_empty(self,faller:Faller):
        'Checks the left 3 spaces of current faller to see if available to move left to'
        return (self.board[faller.count-3][faller.column-1] == 0 and
                self.board[faller.count-2][faller.column-1] == 0 and
                self.board[faller.count-1][faller.column-1] == 0 and
                faller.column!= 0)

    def check_right_3_empty(self,faller:Faller):
        'Checks the right 3 spaces of current faller to see if available to move left to'
        try:
            return (self.board[faller.count-3][faller.column+1] == 0 and
                    self.board[faller.count-2][faller.column+1] == 0 and 
                    self.board[faller.count-1][faller.column+1] == 0)    
        except IndexError:
            pass


    def update_3_jewels(self,faller:Faller,str1:str,str2:str,shift=int):
        'Given 2 slots on the board, replace contents with given strings.'
        self.board[faller.count-3][faller.column+shift] = (str1+'{}'+str2).format(str(faller.contents[-3]))
        self.board[faller.count-2][faller.column+shift] = (str1+'{}'+str2).format(str(faller.contents[-2]))
        self.board[faller.count-1][faller.column+shift] = (str1+'{}'+str2).format(str(faller.contents[-1]))

    def rotate_3_jewels(self,faller:Faller,str1:str,str2:str):
        'Given 3 jewels, update their spaces on the board with appropriate symbols.'
        self.board[faller.count-3][faller.column] = (str1+'{}'+str2).format(str(faller.contents[0])) 
        self.board[faller.count-2][faller.column] = (str1+'{}'+str2).format(str(faller.contents[-2]))
        self.board[faller.count-1][faller.column] = (str1+'{}'+str2).format(str(faller.contents[-1]))

    def empty_3_jewels(self,faller:Faller):
        'You moved 3 jewels either left or right. Now empty the spaces they were previously in.'
        self.board[faller.count-3][faller.column] = 0
        self.board[faller.count-2][faller.column] = 0
        self.board[faller.count-1][faller.column] = 0



    def move_left_4(self,faller:Faller):
        'Moves the faller left on iterations 4 or more.'
        if self.check_left_3_empty(faller):
            try:
                if self.board[faller.count][faller.column-1] == 0:
                    faller.freeze = False
                    self.update_3_jewels(faller,'[',']',-1)
                else:
                    faller.freeze = True
                    self.check_for_freezing(faller)
                    self.update_3_jewels(faller,'|','|',-1)
                self.empty_3_jewels(faller)
                self.faller_moves_left(faller)
                faller.column-=1
            except IndexError:
                faller.freeze = True
                self.check_for_freezing(faller)
                self.update_3_jewels(faller,'|','|',-1)
                self.empty_3_jewels(faller)
                self.faller_moves_left(faller)
                faller.column-=1
    
        else:
            self.faller_moves_left(faller)

    def move_right_4(self,faller:Faller):
        'Moves the faller right on iterations 4 or more.'
        if self.check_right_3_empty(faller):
            try:
                if self.board[faller.count][faller.column+1] == 0:
                    faller.freeze = False
                    self.update_3_jewels(faller,'[',']',1)
                else:
                    faller.freeze = True
                    self.check_for_freezing(faller)
                    self.update_3_jewels(faller,'|','|',1)
                self.empty_3_jewels(faller)
                self.faller_moves_right(faller)
                faller.column+=1
            except IndexError:
                faller.freeze = True
                self.check_for_freezing(faller)
                self.update_3_jewels(faller,'|','|',1)
                self.empty_3_jewels(faller)
                self.faller_moves_right(faller)
                faller.column+=1
        else:
            self.faller_moves_right(faller)
 
        
    def faller_drops_until_ground(self,faller:Faller)->None:
        'This function handles the faller after 3 or more game ticks. It checks for any actions it should do.'
        if faller.should_rotate and faller.freeze == False:
            faller.rotate_faller_contents()
            self.rotate_3_jewels(faller,'[',']')
            self.reset_faller(faller)
        elif faller.should_rotate and faller.freeze == True:
            faller.rotate_faller_contents()
            self.rotate_3_jewels(faller,'|','|')
            self.reset_faller(faller)
        elif faller.move_left:
            self.move_left_4(faller)
        elif faller.move_right:
            self.move_right_4(faller)
        else:
            self.board[faller.count][faller.column] = self.board[faller.count-1][faller.column]
            self.board[faller.count-1][faller.column] = self.board[faller.count-2][faller.column]
            self.board[faller.count-2][faller.column] = self.board[faller.count-3][faller.column]
            self.board[faller.count-3][faller.column] = 0
            self.check_for_freezing(faller)
            self.print_board()
            faller.count+=1

      

    def faller_cannot_move(self,faller:Faller):
        'Checks for the conditions that determine whether faller is still allowed to move or not'
        return (faller.freeze and not faller.should_rotate and not faller.move_left and not faller.move_right)

    def drop_move_rotate_faller(self,faller:Faller):
        '''First, hardcode the first 3 faller drops. Then, when the entire faller is in the board, use
        drop the faller by moving each piece one down.'''

        if self.faller_cannot_move(faller):
            self.faller_freezes(faller)
                  
        elif faller.count == 0: 
            self.bottom_faller_jewel(faller)
           
        elif faller.count == 1:
            self.bottom_2_faller_jewels(faller)
    
        elif faller.count ==2:
            self.bottom_3_faller_jewels(faller)
       
        elif faller.count >=3: 
            self.faller_drops_until_ground(faller)


    
def handle_command(command:str)-> None:
    'Given a command from the user input, take the appropriate game action'
    if command == "R":
        pass #rotate the faller
    else:
        parse_faller(command)

def parse_faller(info:str)->Faller:
    'Given the user input, create a faller with content and column attributes'
    data = info.replace(' ','')
    faller_column = (int(data[1])-1)
    faller_contents = list(data[2:])
    faller = Faller(faller_contents, faller_column)
    return faller

def collect_field_contents(numrows:int,numcols:int)->[[list]]:
    'Given number of rows and columns, returns a 2d list with new board contents'
    list_to_return = []
    for row in range(numrows):
        sublist = []
        input_string = input()
        for string in input_string:
            if string == ' ':
                sublist.append(0)
            else:
                sublist.append(string.strip())
        list_to_return.append(sublist)
    return list_to_return


    










