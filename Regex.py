from .NFA import NFA

star = '*'
line = '|'
dot = '·'
plus = '+'
question = '?'
leftBracket, rightBracket = '(', ')'
alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + \
    [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
    [chr(i) for i in range(ord('0'), ord('9') + 1)] + \
        ['_', '-', '.', '@', '\n', '\\', 'ă', 'â', 'î', 'ș', 'ț', 'Ă', '/', 'Î', ':', 'Ș', 'Ț', '\t']
        
special_alphabet = [star, line, dot, plus, question]
epsilon = ''


class Regex:
    def __init__(self, regex):
        self.regex = regex
    
    @staticmethod
    def getPriority(op):
        if op == line:
            return 1
        elif op == dot:
            return 2
        elif op == star:
            return 3
        elif op == plus:
            return 3
        elif op == question:
            return 3
        else:       # left bracket
            return 0
 
    @staticmethod
    def basicstruct(inputch):   # Regex = a -> NFA
        state1 = 1
        state2 = 2
        basic = NFA(set(), set(), state1, {}, set())
        basic.S = set([inputch])
        basic.setStart(state1)
        basic.addFinal(state2)
        basic.addTransition(state1, state2, inputch)
        return basic  
      
      
    @staticmethod
    def dotstruct(a, b):    # Regex = a.b -> NFA
        [a, m1] = a.newBuildFromNumber(1)
        # print("m1 " + str(m1))
        [b, m2] = b.newBuildFromNumber(m1)
        # print("m2 " + str(m2))
        state1 = 1
        state2 = m2 - 1
        dotFA = NFA(set(), set(), state1, {}, set())
        dotFA.S = a.S.union(b.S)
        dotFA.setStart(state1)
        dotFA.addFinal(state2)
    
        dotFA.K.update(a.K)
        dotFA.K.update(b.K)
       
        dotFA.addTransition(list(a.F)[0], b.q0, epsilon)
        
        dotFA.d.update(a.d)
        dotFA.d.update(b.d)
        
        return dotFA
    
    @staticmethod
    def starstruct(a):  # Regex = a* -> NFA
        [a, m1] = a.newBuildFromNumber(2)
        state1 = 1
        state2 = m1
        starFA = NFA(set(), set(), state1, {}, set())
        starFA.S = a.S
        starFA.d = a.d
        starFA.setStart(state1)
        starFA.addFinal(state2)
        starFA.addTransition(starFA.q0, a.q0, epsilon)
        starFA.addTransition(starFA.q0, list(starFA.F)[0], epsilon)
        starFA.addTransition(list(a.F)[0], list(starFA.F)[0], epsilon)
        starFA.addTransition(list(a.F)[0], a.q0, epsilon)
        
        starFA.K.update(a.K)
       
        return starFA
    
    @staticmethod
    def plusstruct(a):  # Regex = a+ -> NFA
        [a, m1] = a.newBuildFromNumber(2)
        state1 = 1
        state2 = m1
        plusFA = NFA(set(), set(), state1, {}, set())
        plusFA.S = a.S
        plusFA.d = a.d
        plusFA.setStart(state1)
        plusFA.addFinal(state2)
        plusFA.addTransition(plusFA.q0, a.q0, epsilon)
        # plusFA.addTransition(plusFA.q0, list(plusFA.F)[0], epsilon)
        plusFA.addTransition(list(a.F)[0], list(plusFA.F)[0], epsilon)
        plusFA.addTransition(list(a.F)[0], a.q0, epsilon)
        
        plusFA.K.update(a.K)
       
        return plusFA
    
    @staticmethod
    def questionstruct(a):  # Regex = a? -> NFA
        [a, m1] = a.newBuildFromNumber(2)
        state1 = 1
        state2 = m1
        questionFA = NFA(set(), set(), state1, {}, set())
        questionFA.S = a.S
        questionFA.d = a.d
        questionFA.setStart(state1)
        questionFA.addFinal(state2)
        questionFA.addTransition(questionFA.q0, a.q0, epsilon)
        questionFA.addTransition(questionFA.q0, list(questionFA.F)[0], epsilon)
        questionFA.addTransition(list(a.F)[0], list(questionFA.F)[0], epsilon)
        
        questionFA.K.update(a.K)
       
        return questionFA
    
    @staticmethod
    def linestruct(a, b):   # Regex = a|b -> NFA

        [a, m1] = a.newBuildFromNumber(2)
        [b, m2] = b.newBuildFromNumber(m1)
        state1 = 1
        state2 = m2
        
        
        lineFA = NFA(set(), set(), state1, {}, set())
        lineFA.S = a.S.union(b.S)
        
        lineFA.setStart(state1)
        lineFA.addFinal(state2)
        
        lineFA.K.update(a.K)
        lineFA.K.update(b.K)
        
        
        lineFA.addTransition(lineFA.q0, a.q0, epsilon)
       
        lineFA.addTransition(lineFA.q0, b.q0, epsilon)
        lineFA.addTransition(list(a.F)[0], list(lineFA.F)[0], epsilon)
        lineFA.addTransition(list(b.F)[0], list(lineFA.F)[0], epsilon)
        
        lineFA.d.update(a.d)
        lineFA.d.update(b.d)
        
        return lineFA
    
    
    def thompson(self):
        symbol = set()

        escaped = False
        for ch in self.regex:
            if escaped:
                symbol.add(ch)
                escaped = False
            else:   
                if ch == '\\':
                    escaped = True
                
                if ch in alphabet:
                    symbol.add(ch)
                    
        self.automata = []
        
        for ch in self.regex:
            if ch in alphabet:
                self.automata.append(Regex.basicstruct(ch))
                
            elif ch == line:
                if len(self.automata) < 2:
                    continue
                b = self.automata.pop()
                a = self.automata.pop()
                self.automata.append(Regex.linestruct(a, b))
            elif ch == dot:
                if len(self.automata) < 2:
                    continue
                b = self.automata.pop()
                a = self.automata.pop()
                self.automata.append(Regex.dotstruct(a, b))
            elif ch == star:
                if len(self.automata) < 1:
                    continue
                a = self.automata.pop()
                self.automata.append(Regex.starstruct(a))
            elif ch == plus:
                if len(self.automata) < 1:
                    continue
                a = self.automata.pop()
                self.automata.append(Regex.plusstruct(a))
            elif ch == question:
                if len(self.automata) < 1:
                    continue
                a = self.automata.pop()
                self.automata.append(Regex.questionstruct(a))
        self.nfa = self.automata.pop()
        self.nfa.S = symbol
        return self.nfa
        

# you should extend this class with the type constructors of regular expressions and overwrite the 'thompson' method
# with the specific nfa patterns. for example, parse_regex('ab').thompson() should return something like:

# >(0) --a--> (1) -epsilon-> (2) --b--> ((3))

# extra hint: you can implement each subtype of regex as a @dataclass extending Regex


def parse_regex(regex: str) -> Regex:
    
    # create a Regex object by parsing the string

    # you can define additional classes and functions to help with the parsing process
    # dfa = parse_regex(regex).thompson().subset_construction()
    
    # convert infix expression to postfix expression
    
    escaped = False

    
    regex = regex.replace("\\ ", "Ț")
    regex = regex.replace(" ", "")
    regex = regex.replace("\+", "ă")
    regex = regex.replace("\*", "â")
    regex = regex.replace("\(", "î")
    regex = regex.replace("\)", "Î")
    regex = regex.replace("\?", "ș")
    regex = regex.replace("\|", "ț")
    regex = regex.replace("\/", "Ș")
    
    regex = regex.replace("[0-9]", "(0|1|2|3|4|5|6|7|8|9)")
    regex = regex.replace("[a-z]", "(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|w|v|x|y|z)")
    regex = regex.replace("[A-Z]", "(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|W|V|X|Y|Z)")
    regex = regex.replace("[1-9]", "(1|2|3|4|5|6|7|8|9)")
    
    tword = ''
    pre = ''
    
    for ch in regex:
        if ch in alphabet or ch == leftBracket:

            if pre != dot and (pre in alphabet or pre in [star, rightBracket, plus, question]):
                tword += dot
        tword += ch
        pre = ch
    regex = tword

        # convert infix expression to postfix expression
    tword = ''
    stack = []
    
    for ch in regex:
        
        if ch in alphabet:
            tword += ch
        elif ch == leftBracket:
            stack.append(ch)
        elif ch == rightBracket:
            while(len(stack) and stack[-1] != leftBracket):
                
                tword += stack[-1]
                if len(stack):
                    stack.pop()
            if len(stack):
                stack.pop()    # pop left bracket
        else:
            while(len(stack) and Regex.getPriority(stack[-1]) >= Regex.getPriority(ch)):
                tword += stack[-1]
                if len(stack):
                    stack.pop()
            stack.append(ch)
                

    while(len(stack) > 0):
        tword += stack.pop()
    regex = tword
   
    return Regex(regex)


    # pass
