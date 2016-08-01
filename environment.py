class Environment(object):
    """
    This defines the environment that the players play in.
    It will set the penalty for every choice, 
    and the number of games that are played.
    """

    def __init__(self, number_of_iterations, penalty_matrix):
        """ 
        `number_of_iterations` is the number of times that two
        players will have to make their choices.
        `penalty_matrix` is a (2 x 2) matrix of 2-tuples
        """
        self.strategies = []
        self.number_of_iterations = number_of_iterations
        self.penalty_matrix = penalty_matrix

    def play(self, first, second):
        first_player = first()
        second_player = second()
        for _ in xrange(self.number_of_iterations):
            self.round(first_player, second_player)

    def round(self, first_player, second_player):

        choice_first = first_player.choose()
        choice_second = second_player.choose()

        penalty = self.decide_penalty(choice_first, choice_second)
        first_penalty, second_penalty = penalty

        first_player.remember(choice_first, choice_second)
        second_player.remember(choice_second, choice_first)

    def decide_penalty(self, first_choice, second_choice):
        print self.penalty_matrix[first_choice][second_choice]
        return self.penalty_matrix[first_choice][second_choice]

    def add_player(self, new_player):
        # TODO: assert that new_player is of type Player
        self.strategies.append(new_player)

    def round_robin(self):
        first_strategy = self.strategies[0]
        second_strategy = self.strategies[1]
        self.play(first_strategy, second_strategy)

class PlainStrategy(object):

    def __init__(self):
        pass

    def remember(self, my_choice, opponent_choice):
        ''' save the previous choices into your state '''
        pass

    def choose(self):
        ''' choose 1 for confessing and 0 for omerta '''
        return 1

    def refresh(self):
        ''' forget history '''
        pass


class TitForTat(PlainStrategy):

    def __init__(self, *args, **kwargs):
        super(TitForTat, self).__init__(*args, **kwargs)
        self.history = 0

    def remember(self, my_choice, opponent_choice):
        self.history = opponent_choice
        assert(0 <= self.history <= 1)

    def choose(self):
        return self.history

    def refresh(self):
        self.history = 0

penalty_matrix = [[(1, 1), (0, 10)], [(10, 0), (9, 9)]]
env = Environment(500, penalty_matrix)

env.add_player(PlainStrategy)
env.add_player(TitForTat)

env.round_robin()
