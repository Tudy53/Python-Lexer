# Python-Lexer
 The project consists in the implementation of a lexer in python.
 Project
The project consists in the implementation of a lexer in python.

# What is a lexer?
A lexer is a program that divides a string of characters into substrings called lexemes, each of which is classified as a token, based on a specification.

# Which is the input of a Lexer?
The lexer initially receives a specification of the form:
TOKEN1 : REGEX1;
TOKEN2 : REGEX2;
TOKEN3 : REGEX3;

...
where each TOKENi is a name given to a token, and REGEXi is a regex describing lexemes that can be classified as that token. You can think of this specification as a configuration file, which describes how the lexer will work on various text files.
The actual input of a lexer is a text that will be divided into lexemes using regular expressions. In future courses you will learn more details about how lexers work and how they are implemented.

# Which is the output of a lexer?

The lexer outputs a list of the form: [(lexema1, TOKEN_LEXEMA_1), (lexema2, TOKEN_LEXEMA_2), …], where TOKEN_LEXEMA_N is the name of the token associated with lexeme n, based on the specification.

# Stage 1
Due to the difficulty of working directly with regexes to verify the belonging of a word in the language, real lexers go through several intermediate stages before starting the analysis of the text. These steps build a DFA based on the regex.
Stage 1 of the project consists of converting NFA into DFA (using the Subset Construction Algorithm presented in the course)
The theme will be implemented in Python, and the skeleton offers you a pattern for implementing the necessary functionalities.
Structure
# Class DFA
 A DFA will be described by the following fields:
S - the alphabet of the language, represented as a set of strings
K - states of the automaton, represented as a set of __STATE__
q0 - the initial state of the automaton
d - transition function, represented as a dictionary with key (state, character_alphabet) and another state as value
F - the final states of the automaton

Although the simplest way to refer to a state is through an integer, in certain components of the project (and from this stage, but also from future stages) it will be much more convenient to work with other types of tags for states (eg sets of integers or tuples). Therefore, the STATE parameter allows you to use whatever type you want as the state of the automaton, you can note the states of the automaton both with integers 0,1,2,3,... and with character strings s0,q1,sink,... or other types data (frozenset)

1. In this class you will have to implement the accept function, a function that receives a word and running the DFA on that word will return True if the word is accepted, and False otherwise.
2. The remap_states function is not mandatory to implement, since it is not called by the checker, but it is recommended since it will facilitate the implementation of the subset construction algorithm. It aims to transform the set of states, from one type (for example string) to another (for example, integer). Such transformations will be necessary, especially in the later stages of the project.
For example, if we have the next automata:

![image](https://github.com/Tudy53/Python-Lexer/assets/94364533/c1bc0d37-fbb7-4e09-b1f4-b05dd4365e58)

 
We can aply the function a x → 'q' + str(x+2), which would create the next DFA:

![image](https://github.com/Tudy53/Python-Lexer/assets/94364533/dadd5f3a-59cf-4149-9af6-947793007361)

 
# Class NFA
The class works in the same way as the DFA, with one difference:
• Unlike the representation from the course, where ΔΔ represented a relation over K×Σ×K ×Σ× , in Stage 1, d will also be a function, (encoded through a dictionary), which will associate a pair (state, character_alphabet), a set of successor states (instead of a single state, as happens in a DFA).
Other observations:
1. The function epsilon_closure receives a state of the automaton and returns a set of states, which represent the states that can be reached only by epsilon-transitions from the initial state (without consuming any characters)
2. The subset_construction function will return a DFA, built from the current NFA through the subset construction algorithm. The returned DFA will have the state type frozenset[STATE] (states 0 and 1 from an NFA will end up with a set of states {0,1} from a DFA). We use frozenset instead of set, because the latter is not immutable (sets can be modified by side effects). We need an immutable object to be able to calculate a hash (always the same), and implicitly to be able to use such objects as keys in a dictionary (something impossible if the key object is mutable).
3. The remap_states function which has the same format and purpose as the function from DFAs
The epsilon_closure and subset_construction functions must be implemented, and the remap_states function is not.

# Stage 2
 Stage 2 of the project consists of Regex - NFA conversion (using the Thompson Algorithm presented in the course)
# Skeletal structure
In the skeleton of the theme you will find, besides the 2 classes from the previous stages (NFA and DFA), another class, Regex, and a parse_regex method.
The standard form of regular expressions
The standard form of regexes can be described in BNF form as follows:
<regex> ::= <regex><regex> | 
            <regex> '|' <regex> | 
            <regex>'*' | <regex>'+' | <regex>'?' | 
            '(' <regex> ')' | 
            "[A-Z]" |
            "[a-z]" |
            "[0-9]" |
            "eps" | <character> 
In the above description, the elements between angle brackets <> are non-terminals to be generated, characters are always enclosed in single quotes, and strings are enclosed in double quotes.
<character> refers to any regular character that is not a control character (such as * or |), or any string of length two of the form \c, where c can be any character including the control.
"eps" represents the Epsilon character.
# Regex preprocessing
In the description above, in addition to the alpha-numeric characters and the basic operations star, concat and union, you will also find:
1. two new operations:
a. plus + - the expression to which it is applied appears 1 time or more.
b. the question mark? - the expression to which it is applied appears once or never.
2. 3 syntactic sugars:
a. [a-z] - any lower case character in the English alphabet
b. [A-Z] - any uppercase character in the English alphabet
c. [0-9] - any number
If a regex contains white spaces, they are ignored. In order not to be ignored, they will be preceded by a backslash "\". Similarly, in order not to confuse the characters '*', '+', ')', '(', '|', '?' which also represent regex operators, when they are actually part of the regex, they will be preceded of backslashes.
# Regex class
In this class you will have to implement the thompson method, the method that receives a regex type object and returns an NFA (with int type states as a convention). The regex received as input will have the form presented above.
The concatenation will not be represented by a specific character, we will consider that constructions of the form ab are automatically translated into "character a concatenated with character b". The concatenation thus stops at the meeting of a parenthesis or a union. E.g:
1. ab|c is translated into (ab)|c
2. abd* is translated into ab(d)*
3. ab+ is translated into a(b)+
# Stage 3
Stage 3 of the project consists of implementing a lexer in python.
Skeletal structure
In the framework of the theme you will find, besides the 3 classes from the previous stages (Regex, NFA and DFA), another class, Lexer.
# What is a Lexer
A lexer is a program that divides a string of characters into substrings called lexemes, each of which is classified as a token, based on a specification.
There are several ways you can implement a lexer. The conventional approach (and the one we recommend) consists of the following stages:
1. each regex is converted into an AFN, keeping at the same time the information about the related token and the position at which it appears in the spec.
2. a unique AFN is built, introducing an initial state and epsilon-transitions from it to all the initial states of the AFNs above. Thus, this AFN will accept any of the tokens described in the specification. The final state visited will indicate the token found.
3. The AFN is converted to an AFD (which can optionally be minimized). In this machine:
a. when we visit a group of states that contains (AFN-)final states, it means that one or more corresponding tokens have been identified.
b. when we visit a sink-state (if it exists), it means that the current substring is not described by any token. In this case, we must return the longest accepted prefix and continue lexing the remaining word
c. when we visit a non-final state and which is not a sink-state, we continue by passing to the next state of the AFD consuming a character from the word

The purpose of a lexer is to identify the longest substring that satisfies a regex from the given specification. If a longest substring satisfies two or more regexes, the first related token will be reported, in the order in which they are written in the specification.
To identify the longest substring using an AFD like the one described in the previous section, we must note that:
1. visiting a group of states that contains a final (AFN-) state does not necessarily indicate that we have found the longest accepted substring.
2. if a group of states containing a final (AFN-) state has been previously visited:
a. visiting a group of states that does not contain final states does not necessarily indicate that we have found the longest substring (the automaton may accept in the future)
b. visiting the sink-state of the AFD (if it exists), indicates that the machine will no longer accept it in the future.
c. if there is no sink state in AFD, then the lexical analysis must continue until the input is exhausted, to decide on the longest substring.
Once the longest substring has been identified:
1. The AFD will be reset - brought to the initial state to resume the lexical analysis.
2. the lexical analysis will continue from the position where the longest substring has ended, and this can precede the current position where the analysis has reached by any number of positions.

# Lexer class
The lexer class has a constructor that receives as a parameter a specification that has the following structure:
spec = [(TOKEN_LEXEMA_1, regex1), (TOKEN_LEXEMA_2, regex2), ...]
where the first element of each tuple is a name given to a token, and the second element of the tuple is a regex describing that token. You can think of this specification as a configuration file that describes how the lexer will work on various text files.
In addition, the lexer class contains the function lex that will receive a word str as input and return the result of its lexer in the form list[tuple[str, str]]. The method will return a list of tuples (token, lexem_word) if the lexation succeeds. On error, a list with a single element of the form ("", "No viable alternative at character _, line _") will be returned (More on cases where a lexer can fail below). Thus, the method outputs a list of the form: [(TOKEN_LEXEMA_1, lexema1), (TOKEN_LEXEMA_2, lexema2), …], where TOKEN_LEXEMA_N is the name of the token associated with lexeme n, based on the specification.
Exemple
Let it be the next specification:
spec = [("TOKEN1", "abbc*"), ("TOKEN2", "ab+"), ("TOKEN3", "a*d")]
and the abbd input. The lexical analysis will stop at character d (the previously described AFD will reach this character in sink state). The substring abb is the longest that satisfies both TOKEN1 and TOKEN2, and TOKEN1 will be reported, since it precedes TOKEN2 in the specification. Afterwards, the lexer will advance by one character the current position in the input, and will identify the substring d as TOKEN3.
For further clarifications and more examples that include the longest substring, revisit the course on lexers.
# Lexation errors
Lexation errors are generally caused by a wrong / incomplete configuration or an invalid word. The information that must be transmitted in this case must help the programmer to figure out where in a code the error occurred and what is the type of error. For this reason, we will display the line and column where the lexing failed and the type of error. The error is equivalent to reaching the SINK_STATE state of the lexer without first passing through a final state. In this case we will display an error message in the format

No viable alternative at character ..., line ...
In the first free place we will put the index of the character where the lexing stopped (we reached SINK_STATE) indexed from 0, and in the second free space we will put the line where this happened (indexed from 0).
If the lexer has reached the end of the word without first accepting a lexeme, and the lexer has not reached the sync state, but not in a final state either, we will display an error message in the format:
No viable alternative at character EOF, line ...
As a short summary: the first error occurs when the character we reached is invalid and we have no way to accept it, and the second occurs when the lexer would still accept it, but the word is incomplete and has nothing left.
# Testing
Checking the correctness of your implementation will be done automatically, through a series of unit tests, tests that will check the behavior of each mandatory function to be implemented and will test its output on a variety of inputs.
Another preliminary check that will be done on each DFA built will be one that verifies the integrity of the d.p.d.v. structural (the initial state and the final states are included in many states, it does not have defined transitions on a character from a certain state).
# Python
The python version we will use for this theme is python3.12. 
To run the tests, use the python3.12 -m unittest command. This command will automatically detect the tests defined in the test folder and run them one by one, finally displaying the failed tests, if any.

