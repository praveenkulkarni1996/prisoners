class Environment(object):
    '''
    This defines the environment that the players play in.
    It will set the penalty for every choice, 
    and the number of games that are played.
    '''

    def __init__(self, number_of_iterations, penalty_matrix):
        """ 
        `number_of_iterations` is the number of times that two
        players will have to make their choices.
        `penalty_matrix` is a (2 x 2) matrix of 2-tuples
        """
        self.strategies = []
        self.number_of_iterations = number_of_iterations
        self.penalty_matrix = penalty_matrix

    def play(self, first_strategy, second_strategy):
        ''' simulates all rounds of a one-on-one match between 2 strategies '''
        first_player = first_strategy()
        second_player = second_strategy()
        print('---- {} vs {} ----'.format(first_strategy.__name__, second_strategy.__name__))
        for _ in xrange(self.number_of_iterations):
            self.round(first_player, second_player)

    def round(self, first_player, second_player):
        ''' simulates one iteration between two players '''
        choice_first = first_player.choose()
        choice_second = second_player.choose()

        penalty = self.decide_penalty(choice_first, choice_second)
        first_penalty, second_penalty = penalty

        first_player.remember(choice_first, choice_second)
        second_player.remember(choice_second, choice_first)

    def decide_penalty(self, first_choice, second_choice):
        ''' sets the penalty for two players '''
        print self.penalty_matrix[first_choice][second_choice]
        return self.penalty_matrix[first_choice][second_choice]

    def add_strategy(self, new_player):
        ''' adds the strategies to the environment '''
        # TODO: assert that new_player is of type Strategy
        self.strategies.append(new_player)

    def round_robin(self):
        ''' plays a round robin tournament between all strategies '''
        if(len(self.strategies) < 2):
            # TODO: raise too few error
            raise NotImplementedError
        for first_idx, first_strategy in enumerate(self.strategies):
            for second_idx, second_strategy in enumerate(self.strategies):
                if(first_idx < second_idx): break
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

class MutuallyAssuredDestruction(PlainStrategy):

    def __init__(self, *args, **kwargs):
        super(MutuallyAssuredDestruction, self).__init__(*args, **kwargs)
        self.history = 0

    def remember(self, my_choice, opponent_choice):
        if(opponent_choice == 1):
            self.history = 1

    def choose(self):
        return self.history

    def refresh(self):
        self.history = 0

def RandomStrategiesGenerator(confess_probability):
    ''' returns strategy that confesses with `confess_probability` '''

    class RandomStrategy(PlainStrategy):

        @classmethod
        def rename_class(cls, args):
            ''' renames strategies for more verbose information '''
            cls.__name__ = 'RandomStrategy({})'.format(args)

        def __init__(self, *args, **kwargs):
            super(RandomStrategy, self).__init__(*args, **kwargs)
            assert(0 <= confess_probability <= 1)
            self.confess_probability = confess_probability
            RandomStrategy.rename_class(confess_probability)

        def choose(self):
            from random import randint 
            from fractions import Fraction
            ''' 
                Given probability a/b, choose a random number `x`
                in [1, b]. If x lies in [1, a] then confess 
            '''
            frac = Fraction(self.confess_probability).limit_denominator(10000)
            random_number = randint(1, frac.denominator)
            if(random_number <= frac.numerator): return 1
            else: return 0

    return RandomStrategy

penalty_matrix = [[(1, 1), (0, 10)], [(10, 0), (9, 9)]]
env = Environment(10, penalty_matrix)

always_confess_strategy = RandomStrategiesGenerator(1.0)
always_omerta_strategy = RandomStrategiesGenerator(0.0)
confused = RandomStrategiesGenerator(0.5)

# env.add_strategy(TitForTat)
# env.add_strategy(PlainStrategy)
# env.add_strategy(MutuallyAssuredDestruction)

env.add_strategy(always_omerta_strategy)
env.add_strategy(always_confess_strategy)
env.add_strategy(confused)
env.round_robin()
