from game import Game

if __name__ == '__main__':
    ai = True
    load = True
    game = Game(ai, load)
    game.run()
    if ai and input("Do you want to save the Q-table? (y/n): ") == 'y':
        game.save_q_table()
