from collections import defaultdict
from .DFA import DFA

from dataclasses import dataclass
from collections.abc import Callable

EPSILON = ''  # this is how epsilon is represented by the checker in the transition function of NFAs

@dataclass
class NFA[STATE]:
    
    S: set[str] # alphabet
    K: set[STATE] # states
    q0: STATE # initial state
    d: dict[tuple[STATE, str], set[STATE]] # transition function
    F: set[STATE] # final states
       
    def __init__(self):
        self.S = set()
        self.K = set()
        self.q0 = None
        self.d = defaultdict(set)
        self.F = []
        
    def __init__(self, S, K, q0, d, F):
        self.S = S
        self.K = K
        self.q0 = q0
        self.d = d
        self.F = F
        
    def setStart(self, state):
        self.startstate = state
        self.K.add(state)

    def addFinal(self, state):
        if isinstance(state, int):
            state = [state]
        for s in state:
            if s not in self.F:
                self.F.add(s)

    def addTransition(self, fromstate, tostate, inputch):   # add only one transition
        self.K.add(fromstate)
        self.K.add(tostate)
        
        if (fromstate, inputch) in self.d:
            self.d[(fromstate, inputch)].add(tostate)
        else:
            self.d[(fromstate, inputch)] = {tostate}


    def newBuildFromNumber(self, startnum):
    # change the states' representing number to start with the given startnum
        translations = {}
        rebuild = NFA(set(), set(), None, {}, set())
        
        for i in self.K:
            translations[i] = startnum
            rebuild.K.add(startnum)
            startnum += 1
            
        rebuild.S = self.S
        rebuild.q0 = translations[self.q0]
        rebuild.F.add(translations[list(self.F)[0]])
        rebuild.K.add(translations[list(self.F)[0]])
        
        for (fromstate, character), tostates in self.d.items():
            for state in tostates:
                rebuild.addTransition(translations[fromstate], translations[state], character)
       
        return [rebuild, startnum]

    def epsilon_closure(self, state: STATE) -> set[STATE]:
        epsilon_set = set()
        visited_states = set()
        stack = [state]

        while stack:
            current_state = stack.pop()

            if current_state in visited_states:
                continue

            visited_states.add(current_state)
            epsilon_set.add(current_state)

            epsilon_transitions = self.d.get((current_state, EPSILON), set())
            stack.extend(epsilon_transitions - visited_states)

        return epsilon_set

    def subset_construction(self) -> DFA[frozenset[STATE]]:
        new_states = set()
        new_transitions = dict()
        new_initial = frozenset(self.epsilon_closure(self.q0))
        new_finals = set()

        queue = [new_initial]
        visited = set()

        while queue:
            current_set = queue.pop()
            if current_set not in visited:
                visited.add(current_set)
                new_states.add(current_set)

                for symbol in self.S:
                    next_states = set()
                    for state in current_set:
                        next_states.update(self.d.get((state, symbol), set()))

                    epsilon_closure_result = set()
                    for next_state in next_states:
                        epsilon_closure_result.update(self.epsilon_closure(next_state))

                    next_set = frozenset(epsilon_closure_result)

                    new_transitions[(current_set, symbol)] = next_set
                    if next_set not in visited:
                        queue.append(next_set)

        for final_state in self.F:
            for state_set in new_states:
                if final_state in state_set:
                    new_finals.add(state_set)

        return DFA(
            S=self.S,
            K=new_states,
            q0=new_initial,
            d=new_transitions,
            F=new_finals
        )
    
    

    def remap_states[OTHER_STATE](self, f: 'Callable[[STATE], OTHER_STATE]') -> 'NFA[OTHER_STATE]':
        # optional, but may be useful for the second stage of the project. Works similarly to 'remap_states'
        # from the DFA class. See the comments there for more details.
        pass
    