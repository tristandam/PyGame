#Tristan Dam 12129189
# columns_ui.py

import columns
from columns import Gamestate, Faller


def user_interface()->None:
        numrows = int(input())
        numcols = int(input())
        field_command = input()
        if field_command == "EMPTY":
            game = Gamestate(numrows, numcols)
        else:
            game = Gamestate(numrows, numcols)
            field_contents = columns.collect_field_contents(numrows,numcols)
            game.mutate_board(field_contents)
        game.drop_jewels()
        game.print_board()
        while True:
            action = input()
            if action == "Q" or game.game_active == False:
                break
            if action == '':# and faller.active:
                game.drop_move_rotate_faller(faller)
            if len(action) ==9:#  and faller.active == False:
                    faller = columns.parse_faller(action)
                    game.drop_move_rotate_faller(faller)
            if action == "R":
                faller.should_rotate = True
                game.drop_move_rotate_faller(faller)
            if action == ">":
                faller.move_right = True
                game.drop_move_rotate_faller(faller)
            if action == "<":
                faller.move_left = True
                game.drop_move_rotate_faller(faller)
            
                    
            
if __name__ == '__main__':
    user_interface()
