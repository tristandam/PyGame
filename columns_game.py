#Tristan Dam 12129189
#columns_game.py

import pygame
import columns
import random

initial_width = 600
initial_height = 900
background_color = pygame.Color(255,255,255)
line_color = pygame.Color(0,0,0)
frame_rate = 8
board_rows = 13
board_columns = 6

s_color = pygame.Color(51,0,255) #blue
t_color = pygame.Color(54,167,227) #teal
v_color = pygame.Color(35,232,58) #green
w_color = pygame.Color(87,64,16) #brown
x_color = pygame.Color(201,58,175) #purple
y_color = pygame.Color(199,197,90) #yellow
z_color = pygame.Color(0,0,0) #black
fall_color = pygame.Color(255,0,0)



class ColumnsGame:
    def __init__(self):
        self.running = True
        self.state = columns.Gamestate(13,6)
        self.faller = columns.Faller(self.random_faller_contents(),self.random_faller_column())

    def random_faller_contents(self)->list:
        'Randomly generates a list of 3 jewel colors for the faller'
        valid_jewels = 'STVWXYZ'
        result = []
        for i in range(3):
            result.append(random.choice(valid_jewels))
        return result

    def random_faller_column(self)->int:
        'Randomly generate a column for the faller to drop in'
        return random.randint(0,5)

    def create_surface(self, size: (int,int)) -> None:
        self.surface = pygame.display.set_mode(size, pygame.RESIZABLE)
    
    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        self.create_surface((initial_width,initial_height))
        count = 0
        while self.running:
            if self.state.game_active == False:
                self.running = False
            clock.tick(frame_rate)
            self.handle_events() #this handles things like rotating, moving left and right.
            if self.faller.active:
                self.state.drop_move_rotate_faller(self.faller)
            else:
                self.faller = columns.Faller(self.random_faller_contents(),self.random_faller_column())
                self.state.drop_move_rotate_faller(self.faller)
            self.draw_frame()
            

        pygame.quit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            self.handle_event(event)

        self.handle_keys()

    def handle_event(self, event) -> None:
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.VIDEORESIZE:
            self.create_surface(event.size)

    def handle_keys(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.faller.move_left = True
        if keys[pygame.K_RIGHT]:
            self.faller.move_right = True
        if keys[pygame.K_SPACE]:
            self.faller.should_rotate = True


    def draw_frame(self) -> None:
        self.surface.fill(background_color)
        self.draw_grid()
        self.draw_jewels()
        pygame.display.flip()

    def draw_grid(self) -> None:
        width = self.surface.get_width()
        height = self.surface.get_height()
        dx = width/board_columns
        dy = height/board_rows
        for c in range(1,board_columns):
            pygame.draw.line(self.surface, line_color, (c*dx,0),(c*dx,height))
        for c in range(1,board_rows):
            pygame.draw.line(self.surface, line_color, (0,c*dy),(width,c*dy))





    def draw_jewels(self) -> None:
        width = self.surface.get_width()
        height = self.surface.get_height()
        dx = width/board_columns
        dy = height/board_rows
        jewel_list = ['S','T','V','W','X','Y','Z']
        jewel_list_bracket = ['[S]','[T]','[V]','[W]','[X]','[Y]','[Z]']
        color_list = [s_color,t_color,v_color,w_color,x_color,y_color,z_color]
        falling_jewel_list = ['|S|','|T|', '|V|','|W|','|X|','|Y|','|Z|']
        
        for row in range(len(self.state.board)):
            for column in range(board_columns):
                top_left_x = column*dx
                top_left_y = row*dy
                jewel_rect = pygame.Rect((top_left_x,top_left_y),(dx,dy))
                
                for i in range(len(jewel_list_bracket)):
                    if (self.state.board[row][column]==jewel_list_bracket[i]):
                        self.draw_jewel(color_list[i],jewel_rect)

                for i in range(len(jewel_list)):
                    if (self.state.board[row][column]==jewel_list[i]):
                        self.draw_jewel(color_list[i],jewel_rect)

                for i in range(len(falling_jewel_list)):
                    if (self.state.board[row][column]==falling_jewel_list[i]):
                        self.draw_jewel(fall_color,jewel_rect)
                    
    def draw_jewel(self,color:pygame.Color,rect:pygame.Rect) -> None:
        pygame.draw.rect(self.surface, color,rect)


    def draw_falling_jewel(self,color:pygame.Color,rect:pygame.Rect) -> None:
         pygame.draw.rect(self.surface, color,rect, width=1000)       

                
        


if __name__ == '__main__':
    ColumnsGame().run()
