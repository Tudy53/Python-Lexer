from src.NFA import NFA
from src.Regex import Regex
from src.Regex import parse_regex
from src.DFA import DFA

EPSILON = ''  # This is how epsilon is represented in the transition function of NFAs

class Lexer:
    def __init__(self, spec: list[tuple[str, str]]) -> None:
        nfas = []
        info = {}
      

        for token_name, regex in spec:
            # print(token_name, regex)
            nfa = parse_regex(regex).thompson()
            nfas.append(nfa)

        
        maximum = len(nfas) - 1
       
        for index in range(0, maximum):
            translations = {}

            startnum = max(list(nfas[index].K)) + 1

            rebuild = NFA(set(), set(), None, {}, set())

            for i in nfas[index + 1].K:
                translations[i] = startnum
                rebuild.K.add(startnum)
                startnum += 1
                

            rebuild.S = nfas[index + 1].S
            rebuild.q0 = translations[nfas[index + 1].q0]
            rebuild.F.add(translations[list(nfas[index + 1].F)[0]])
            rebuild.K.add(translations[list(nfas[index + 1].F)[0]])

            for (fromstate, character), tostates in nfas[index + 1].d.items():
                for state in tostates:
                    rebuild.addTransition(translations[fromstate], translations[state], character)

            nfas[index + 1] = rebuild
        
        index = 0
        nfa_index = 0
        for token_name, regex in spec:
            nfa = nfas[nfa_index]
            nfa_index += 1
            for final_state in nfa.F:
                info[final_state] = (token_name, index)
            index += 1

        start_state = 0
        final_nfa = NFA(set(), set(), None, dict(), set())
        final_nfa.d[(start_state, EPSILON)] = set()
        final_nfa.q0 = start_state
        final_nfa.K.add(start_state)

        for nfa_smol in nfas:
            for state in nfa_smol.K:
                final_nfa.K.add(state)

            for state in nfa_smol.F:
                final_nfa.F.add(state)

            final_nfa.S.update(nfa_smol.S)

            final_nfa.d.update(nfa_smol.d)

            final_nfa.d[(start_state, EPSILON)].add(nfa_smol.q0)

        self.nfa = final_nfa
        my_dfa = final_nfa.subset_construction()
        self.dfa = my_dfa
        self.info = info
   
    
        for alpha in self.dfa.S:
            if alpha == "Ț":
                self.dfa.S.remove(alpha)
                self.dfa.S.add(" ")
                
            if alpha == "Ș":
                self.dfa.S.remove(alpha)
                self.dfa.S.add("/")
                
            if alpha == "ă":
                self.dfa.S.remove(alpha)
                self.dfa.S.add("+")
                
                
            if alpha == "â":
                self.dfa.S.remove(alpha)
                self.dfa.S.add("*")
                
            if alpha == "î":
                self.dfa.S.remove(alpha)
                self.dfa.S.add("(")
                
            if alpha == "Î":
                self.dfa.S.remove(alpha)
                self.dfa.S.add(")")
                
            if alpha == "ș":
                self.dfa.S.remove(alpha)
                self.dfa.S.add("?")
                
            if alpha == "ț":
                self.dfa.S.remove(alpha)
                self.dfa.S.add("|")
                     

        items = list(self.dfa.d.items())
        for (state, str_value), destinations in items:
            if str_value == "Ț":
                self.dfa.d[(state, ' ')] = destinations
                del self.dfa.d[(state, str_value)]
                
            if str_value == "Ș":
                self.dfa.d[(state, '/')] = destinations
                del self.dfa.d[(state, str_value)]  
            
            if str_value == "ă":
                self.dfa.d[(state, '+')] = destinations
                del self.dfa.d[(state, str_value)]
                
            if str_value == "â":
                self.dfa.d[(state, '*')] = destinations
                del self.dfa.d[(state, str_value)]
                
            if str_value == "î":
                self.dfa.d[(state, '(')] = destinations
                del self.dfa.d[(state, str_value)]
                
            if str_value == "Î":
                self.dfa.d[(state, ')')] = destinations
                del self.dfa.d[(state, str_value)]
                
            if str_value == "ș":
                self.dfa.d[(state, '?')] = destinations
                del self.dfa.d[(state, str_value)]
                
            if str_value == "ț":
                self.dfa.d[(state, '|')] = destinations
                del self.dfa.d[(state, str_value)]
                
                

    def lex(self, word: str) -> list[tuple[str, str]] | None:
        matches = []
        index = 0

        while index < len(word):
            state_set = self.dfa.q0
            remaining_input = word[index:]
            built_string = ""
            best_match = ""
            current_token = ""
            while(state_set is not None):
                final_states_in_set = list(set(self.info.keys()) & state_set)
                if final_states_in_set:
                    current_token = self.info[min(final_states_in_set)][0]
                    best_match = built_string
                if remaining_input:
                    next_state_set = self.dfa.d.get((state_set, remaining_input[0]))
                    state_set = next_state_set
                    built_string += remaining_input[0]
                    remaining_input = remaining_input[1:]
                else:
                    break
            if not best_match:
                break
            matches.append((current_token, best_match))
            index += len(best_match)

        position = 0
        while position < len(word):
            max_match_length = 0
            matched = False
            
            current_pos = self.dfa.q0
            last_accepting_pos = -1
            for idx in range(position, len(word)):
                current_char = word[idx]
                subsequent_state = self.dfa.d.get((current_pos, current_char))

                if subsequent_state is None:
                    break
                current_pos = subsequent_state
                if current_pos in self.dfa.F:
                    last_accepting_pos = idx

            self.final_state = current_pos
            match_length =  last_accepting_pos - position + 1
    
            
            if match_length > max_match_length:
                max_match_length = match_length
                matched = True
                
                
            line_start = word.rfind('\n', 0, position)
            line_number = word.count('\n', 0, position)
            char_position = position - line_start
            

            if position + 1 == len(word) and not matched and word[position] in self.dfa.S:
                return [("", f"No viable alternative at character EOF, line {line_number}")]
            if max_match_length == 0:
                if word[position] in self.dfa.S:
                    return [("", f"No viable alternative at character {char_position}, line {line_number}")]
                else:
                    return [("", f"No viable alternative at character {position}, line {line_number}")]

            position += max_match_length

        return matches
