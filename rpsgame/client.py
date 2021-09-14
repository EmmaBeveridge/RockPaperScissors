
import script

script.main()



import pygame
from network import Network
import pickle
from random import randrange

pygame.font.init()


win_width=800
win_height=800
win= pygame.display.set_mode((win_width, win_height), pygame.RESIZABLE)
pygame.display.set_caption("Client")


class Button:
    def __init__(self, text, x_coor, y_coor, button_width, button_height, colour):
        self.text=text
        self.x_coor=x_coor
        self.y_coor=y_coor
        self.colour=colour
        self.width=button_width
        self.height=button_height
        

    def draw_button(self, win):
        pygame.draw.rect(win, self.colour, ((self.x_coor, self.y_coor, self.width, self.height)))
        font=pygame.font.SysFont("arial", 40)
        text=font.render(self.text, 1, (255,255,255) )
        text_pos=(self.x_coor+round(self.width/2)-round(text.get_width()/2), self.y_coor + round(self.height/2)-round(text.get_height()/2))
        win.blit(text,text_pos )
    
    def was_clicked(self, mouse_pos):
        mouse_x= mouse_pos[0]
        mouse_y= mouse_pos[1]
        
        if self.x_coor<=mouse_x<=self.x_coor+self.width and self.y_coor<=mouse_y<=self.y_coor+self.height:
            return True

        else:
            return False




def redraw_win(win, game, player_num, buttons, player_wins, player_loss):
    win.fill((0,0,0))#set window colour
    if not (game.are_players_connected()):
        font=pygame.font.SysFont("arial", 90)
        text=font.render("Waiting for Player...", 1, (255,255,255))
        win.blit(text,( (pygame.display.get_window_size()[0])/2- text.get_width()/2, (pygame.display.get_window_size()[1])/2-text.get_height()/2))
    
    else: #if both players connected
        
        
        font=pygame.font.SysFont("arial", 45)
        
        text=font.render("Your Move", 1, (255,255,255))
        win.blit(text, ( ((pygame.display.get_window_size()[0])//3)-(text.get_width()/2) , ((pygame.display.get_window_size()[1])//4)-(text.get_height()/2) ) )
        
        text=font.render("Opponent's Move", 1, (255,255,255))
        win.blit(text, ( (2*((pygame.display.get_window_size()[0])//3))-(text.get_width()/2) , ((pygame.display.get_window_size()[1])//4)-(text.get_height()/2) ) )
        
        


        player_1_move=game.get_player_move(0)
        player_2_move=game.get_player_move(1)
        if game.have_both_players_been():
            player_1_move_text=font.render(player_1_move, 1, (255,255,255))
            player_2_move_text=font.render(player_2_move, 1, (255,255,255))
        else:
            if player_num==0 and game.p1_went:
                player_1_move_text=font.render(player_1_move, 1, (255,255,255))
            elif game.p1_went: #and player_num==1 is implied
                player_1_move_text=font.render("Selected Move", 1, (255,255,255))
            else: #player_num==1 and not p1_went
                player_1_move_text=font.render("Selecting...", 1, (255,255,255))

            if player_num==1 and game.p2_went:
                player_2_move_text=font.render(player_2_move, 1, (255,255,255))
            elif game.p2_went: #and player_num==0 is implied
                player_2_move_text=font.render("Selected Move", 1, (255,255,255))
            else: #player_num==0 and not p2_went
                player_2_move_text=font.render("Selecting...", 1, (255,255,255))

        
        if player_num==0:
            win.blit(player_1_move_text, ( ((pygame.display.get_window_size()[0])//3)-(player_1_move_text.get_width()/2) , (2*((pygame.display.get_window_size()[1])//4))-(player_1_move_text.get_height()/2) ))
            win.blit(player_2_move_text, ( (2*((pygame.display.get_window_size()[0])//3))-(player_2_move_text.get_width()/2) , (2*((pygame.display.get_window_size()[1])//4))-(player_2_move_text.get_height()/2) ) )

        else:
            win.blit(player_2_move_text, ( ((pygame.display.get_window_size()[0])//3)-(player_2_move_text.get_width()/2) , (2*((pygame.display.get_window_size()[1])//4))-(player_2_move_text.get_height()/2) ))
            win.blit(player_1_move_text, ( (2*((pygame.display.get_window_size()[0])//3))-(player_1_move_text.get_width()/2) , (2*((pygame.display.get_window_size()[1])//4))-(player_1_move_text.get_height()/2) ) )
        
        for button in buttons:
            button.x_coor=((buttons.index(button)+1)*((pygame.display.get_window_size()[0])//4))-(button_width//2)
            button.y_coor=(3*((pygame.display.get_window_size()[1])//4))-(button_height//2)
            button.width=pygame.display.get_window_size()[0]/6
            button.draw_button(win)
        

        font=pygame.font.SysFont("arial", 15)
        
        win_count_text="Won: "+str(player_wins)+" rounds"
        lost_count_text="Lost: "+str(player_loss)+" rounds"
        
        win_text=font.render(win_count_text, 1, (255,255,255))
        lost_text=font.render(lost_count_text, 1, (255,255,255))
        
        win.blit(win_text, ( (pygame.display.get_window_size()[0])-(win_text.get_width()), ((win_text.get_height() ) ) ) )
        win.blit(lost_text, ( (pygame.display.get_window_size()[0])-(lost_text.get_width()), (2*(lost_text.get_height() ) ) ) ) 

    pygame.display.update()


                


button_width=150
button_height=100

rock_button=Button("Rock", ((pygame.display.get_window_size()[0])//4)-(button_width//2), (3*((pygame.display.get_window_size()[1])//4))-(button_height//2), button_width, button_height, (255,0,0) )
paper_button=Button("Paper", (2*((pygame.display.get_window_size()[0])//4))-(button_width//2), (3*((pygame.display.get_window_size()[1])//4))-(button_height//2), button_width, button_height, (0,255,0) )
scissors_button=Button("Scissors", (3*((pygame.display.get_window_size()[0])//4))-(button_width//2), (3*((pygame.display.get_window_size()[1])//4))-(button_height//2), button_width, button_height, (0,0,255) )

buttons=[rock_button, paper_button, scissors_button]


p2_is_user_button=Button("Play Against User", ((pygame.display.get_window_size()[0])//2)-(button_width//2), ((2*(pygame.display.get_window_size()[1])//5))-(button_height//2), button_width, button_height, (0,255,0) )
p2_is_comp_button=Button("Play Against Computer", ((pygame.display.get_window_size()[0])//2)-(button_width//2), ((3*(pygame.display.get_window_size()[1])//5))-(button_height//2), button_width, button_height, (0,255,0) )
exit_button=Button("Exit", ((pygame.display.get_window_size()[0])//2)-(button_width//2), (4*((pygame.display.get_window_size()[1])/4))-(button_height//5), button_width, button_height, (255,0,0) )

menu_buttons=(p2_is_user_button, p2_is_comp_button, exit_button)




def main(buttons):
    run=True
    clock=pygame.time.Clock()
    network=Network()
    player_num=int(network.get_player_num())
    print("You are player", player_num)
    player_wins=0
    player_loss=0
    while run:

        clock.tick(60)
        try:
            game=network.send_data_to_server("get") #sends request to server to get game object
        except:
            run=False
            print("Could not get game")
            break
        if game.have_both_players_been():
            redraw_win(win, game, player_num, buttons, player_wins, player_loss)
            pygame.time.delay(500)
            try:
                game=network.send_data_to_server("reset")
            except:
                run=False
                print("Could not get game")
                break
            font=pygame.font.SysFont("arial", 90)
            if int(game.winner()) == int(player_num):
                player_wins+=1
                text= font.render("You Won!", 1, (255,255,255) )
            elif int(game.winner()) == -1:
                text= font.render("Tie Game!", 1, (255,255,255) )
            else:
                player_loss+=1
                text= font.render("You Lost!", 1, (255,255,255) )
            
            win.blit(text, ((pygame.display.get_window_size()[0])/2- text.get_width()/2, (3*(pygame.display.get_window_size()[1])/5)-text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                
                mouse_pos=pygame.mouse.get_pos()
                

                for button in buttons:
                    
                    button.x_coor=((buttons.index(button)+1)*((pygame.display.get_window_size()[0])//4))-(button_width//2)
                    button.y_coor=(3*((pygame.display.get_window_size()[1])//4))-(button_height//2)
                    button.width=pygame.display.get_window_size()[0]/6
                    
                    if button.was_clicked(mouse_pos) and game.game_ready:
                        
                        if player_num==0:
                            if not game.p1_went:
                            
                                network.send_data_to_server(button.text)

                        else: #if not player 0, must be player 1
                            if not game.p2_went:
                                
                                network.send_data_to_server(button.text)
                                
        redraw_win(win, game, player_num, buttons, player_wins, player_loss)




def menu_screen(menu_buttons, buttons):
    p2_is_user_button, p2_is_comp_button, exit_button=menu_buttons
    run=True
    clock=pygame.time.Clock()
    while run:
        clock.tick(60)
        win.fill((0,0,0))
        font=pygame.font.SysFont("arial", 80)
        text=font.render("Main Menu",1,(255,255,255))
        win.blit(text, ( ((pygame.display.get_window_size()[0])//2)-(text.get_width()/2) , (((pygame.display.get_window_size()[1])//8))-(text.get_height()/2) ))

        font=pygame.font.SysFont("arial", 40)
        text=font.render("Please select an option",1,(255,255,255))
        win.blit(text, ( ((pygame.display.get_window_size()[0])//2)-(text.get_width()/2) , ((2*(pygame.display.get_window_size()[1])//8))-(text.get_height()/2) ))

        for button in menu_buttons:
            button.x_coor=((pygame.display.get_window_size()[0])//3)-(button_width//2)
            button.y_coor=((menu_buttons.index(button)+2)*(pygame.display.get_window_size()[1])//5)-(button_height//2)
            button.width=pygame.display.get_window_size()[0]/2
            button.draw_button(win)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()
            
            if event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()

                for button in menu_buttons:
                    button.x_coor=((pygame.display.get_window_size()[0])//3)-(button_width//2)
                    button.y_coor=((menu_buttons.index(button)+2)*(pygame.display.get_window_size()[1])//5)-(button_height//2)
                    button.width=pygame.display.get_window_size()[0]/2

                if exit_button.was_clicked(mouse_pos):
                    run=False
                    pygame.quit()
                
                elif p2_is_user_button.was_clicked(mouse_pos):
                    run=False
                    main(buttons)

                elif p2_is_comp_button.was_clicked(mouse_pos):
                    run=False
                    play_as_computer(buttons, 0, 0)


    


def play_as_computer(buttons, player_wins, player_loss):
    run=True
    clock=pygame.time.Clock()
    moves=["Rock", "Paper", "Scissors"]
    comp_move=moves[randrange(0,3)]

    player_num=0
    player_been=False
    player_move=None
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                
                mouse_pos=pygame.mouse.get_pos()
                

                for button in buttons:
                    
                    button.x_coor=((buttons.index(button)+1)*((pygame.display.get_window_size()[0])//4))-(button_width//2)
                    button.y_coor=(3*((pygame.display.get_window_size()[1])//4))-(button_height//2)
                    button.width=pygame.display.get_window_size()[0]/6
                    
                    if button.was_clicked(mouse_pos) and not(player_been):
                        player_been=True
                        player_move=button.text
                        
        redraw_win_for_comp_game(win, player_been, player_wins, player_loss, player_move, comp_move)
        
        if player_been:
            player_wins, player_loss=display_winner(comp_move, player_move, player_wins, player_loss)
        
        play_as_computer(buttons, player_wins, player_loss)




def redraw_win_for_comp_game(win, player_been, player_wins, player_loss, player_move, comp_move):
    win.fill((0,0,0))
    font=pygame.font.SysFont("arial", 45)
        
    text=font.render("Your Move", 1, (255,255,255))
    win.blit(text, ( ((pygame.display.get_window_size()[0])//3)-(text.get_width()/2) , ((pygame.display.get_window_size()[1])//4)-(text.get_height()/2) ) )
    
    text=font.render("Computer's Move", 1, (255,255,255))
    win.blit(text, ( (2*((pygame.display.get_window_size()[0])//3))-(text.get_width()/2) , ((pygame.display.get_window_size()[1])//4)-(text.get_height()/2) ) )
    
    if player_been:
        player_1_move_text=font.render(player_move, 1, (255,255,255))
        comp_move_text=font.render(comp_move, 1, (255,255,255))
    else:
        player_1_move_text=font.render("Selecting", 1, (255,255,255))
        comp_move_text=font.render("Selected Move", 1, (255,255,255))
    win.blit(player_1_move_text, ( ((pygame.display.get_window_size()[0])//3)-(player_1_move_text.get_width()/2) , (2*((pygame.display.get_window_size()[1])//4))-(player_1_move_text.get_height()/2) ))
    win.blit(comp_move_text, ( (2*((pygame.display.get_window_size()[0])//3))-(comp_move_text.get_width()/2) , (2*((pygame.display.get_window_size()[1])//4))-(comp_move_text.get_height()/2) ) )

    for button in buttons:
        button.x_coor=((buttons.index(button)+1)*((pygame.display.get_window_size()[0])//4))-(button_width//2)
        button.y_coor=(3*((pygame.display.get_window_size()[1])//4))-(button_height//2)
        button.width=pygame.display.get_window_size()[0]/6
        button.draw_button(win)

    font=pygame.font.SysFont("arial", 15)
    
    win_count_text="Won: "+str(player_wins)+" rounds"
    lost_count_text="Lost: "+str(player_loss)+" rounds"
    
    win_text=font.render(win_count_text, 1, (255,255,255))
    lost_text=font.render(lost_count_text, 1, (255,255,255))
    
    win.blit(win_text, ( (pygame.display.get_window_size()[0])-(win_text.get_width()), ((win_text.get_height() ) ) ) )
    win.blit(lost_text, ( (pygame.display.get_window_size()[0])-(lost_text.get_width()), (2*(lost_text.get_height() ) ) ) ) 

    pygame.display.update()
        
def display_winner(comp_move, player_move, player_wins, player_loss):
    
    font=pygame.font.SysFont("arial", 90)
    if player_move.upper()[0]+comp_move.upper()[0] in ["RS", "SP", "PR"]:
        player_wins+=1
        text= font.render("You Won!", 1, (255,255,255) )
    elif player_move==comp_move:
        text= font.render("Tie Game!", 1, (255,255,255) )
    else:
        player_loss+=1
        text= font.render("You Lost!", 1, (255,255,255) )
    
    win.blit(text, ((pygame.display.get_window_size()[0])/2- text.get_width()/2, (3*(pygame.display.get_window_size()[1])/5)-text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(2000)
    
    return (player_wins, player_loss)

    




while True:
    menu_screen(menu_buttons, buttons)