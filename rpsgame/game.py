class Game:
    def __init__(self, gameId):

        self.p1_went=False
        self.p2_went=False
        self.game_ready=False
        self.game_id=gameId
        self.player_moves=[None, None]
        
        self.ties=0
    
    def get_player_move(self, player):
        return self.player_moves[player]

    def play(self, player_num, move):
        #update self.player_moves[player] with entered move
        self.player_moves[player_num]=move
        if player_num==0:
            self.p1_went=True
        else:
            self.p2_went=True

    def are_players_connected(self):
        #returns if both players connected to game
        return self.game_ready

    def have_both_players_been(self):
        both_been= (self.p1_went and self.p2_went)
        return both_been
    
    def winner(self):
        p1_move=self.player_moves[0].upper()[0] #change move str into either R, P, S
        p2_move=self.player_moves[1].upper()[0]
        
        if p1_move==p2_move:
            winner=-1
        elif (p1_move+p2_move) in ("PR", "RS", "SP"):
            winner=0
        else:
            winner=1
        
        return winner

    def reset_game(self):
        self.p1_went=False
        self.p2_went=False

 


        

