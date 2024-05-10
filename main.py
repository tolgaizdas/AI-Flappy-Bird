from game import Game

if __name__ == '__main__':
    game = Game(ai=True, load=True)
    game.run()
    if input("Do you want to save the Q-table? (y/n): ") == 'y':
        game.save_q_table()
