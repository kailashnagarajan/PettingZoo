from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector
from gym import spaces

from tictactoe_utils import Board

class env(AECEnv):
    metadata = {'render.modes': ['human']} # only add if environment supports rendering

    def __init__(self):
        super(env, self).__init__()
        self.board = Board()

        self.num_agents = 2
        self.agents = list(range(self.num_agents))

        self.agent_order = list(self.agents)
        self._agent_selector = agent_selector(self.agent_order)


        self.action_spaces = {i: spaces.Discrete(9) for i in range(2)}
        self.observation_spaces = {i: spaces.Discrete(9) for i in range(2)}

        self.rewards = {i: 0 for i in range(self.num_agents)}
        self.dones = {i: False for i in range(self.num_agents)}
        self.infos = {i: {'legal_moves': []} for i in range(self.num_agents)}

        self.agent_selection = 0

        self.reset()


    # returns a flat representation of tic tac toe board
    # ie [1, 0, 0, 0, 0, 0, 0, 2, 0]
    # where indexes are column wise order
    # 1 4 7
    # 2 5 8
    # 3 6 9
    # 
    # Key
    # ----
    # blank space = 0
    # agent 0 = 1
    # agent 1 = 2
    def observe(self, agent):
        # return observation of an agent
        return [box.state for box in self.board.boxes]

    # action in this case is a value from 0 to 8 indicating position to move on tic tac toe board
    def step(self, action, observe=True):
        # check if input action is a valid move
        if(self.board.boxes[action] == 0):
            # play turn
            self.board.play_turn(self.board.boxes[action])

            # check if game over
            game_over = all(box.state in [1, 2] for box in self.boxes)

            # if winner = 0 no winner yet
            # if winner = 1 agent 0 won
            # if winner = 2 agent 1 won
            winner = self.board.check_for_winner()

            if game_over:
                if winner == 0:
                    pass
                elif winner == 1:
                    # agent 0 won
                    pass 
                else:
                    # agent 1 won
                    pass
        else:
            # invalid move, some sort of negative reward
            pass

        # Switch selection to next agents
        self.agent_selection = self._agent_selector.next()

        if observe:
            return self.observe(self.agent_selection)
        else:
            return

    # last is added as a part of the AECEnv class, don't write it yourself

    def reset(self, observe=True):
        # reset environment
        self.board = Board()

        # selects the first agent
        self._agent_selector.reinit(self.agent_order)
        self.agent_selection = self._agent_selector.next()
        if observe:
            return self.observe(self.agent_selection)
        else:
            return

    def render(self, mode='human'): # not all environments will support rendering
        pass

    def close(self):
        pass