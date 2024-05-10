from game import Game

if __name__ == '__main__':
    ai = True
    game = Game(discount_factor=0.8, epsilon=0,
                learning_rate=0.2, ai=ai, load=True)
    game.run()
    if ai and input("Do you want to save the Q-table? (y/n): ") == 'y':
        game.q.save_q_table()
