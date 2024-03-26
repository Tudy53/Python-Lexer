from sys import argv
from src.Lexer import Lexer
import re

my_operations = ['lambda', '+', '++']

def main():
    if len(argv) != 2:
        return

    filename = argv[1]
    try:
        with open(filename, 'r') as file:
            code = file.read()
        spec = [
            ("LAMBDA", "lambda"),
            ("CONCAT", r"\+\+"),
            ("PLUS", r"\+"),
            ("EMPTY_LIST", r"\(\)"),
            ("LPAREN", r"\("),
            ("RPAREN", r"\)"),
            ("NUMBER", "([1-9][0-9]*)|0"),
            ("IDENTIFIER", "([a-z]|[A-Z])+"),
            ("WHITESPACE", r"\ "),
            ("NEWLINE", "\n"),
            ("TAB", "\t"),
            ("COLON", ":")
        ]
        lexer = Lexer(spec)
        # print(lexer)
        tokens = lexer.lex(code)
        # print(tokens)
        if tokens is None:
            print("Lexing error")
            return
        parse_input_tokens(tokens)
        
        rez = parse_input_tokens(tokens)

        print(rez)
        
        
    except Exception as e:
        print(f"Error: {e}")


def parse_input_tokens(my_inp):
    list_of_symbols = []

    for i in range(len(my_inp)):
        list_of_symbols.append(my_inp[i][1])

    inp_str = ""
    for i in range(len(list_of_symbols)):
        if list_of_symbols[i] != '\n' and list_of_symbols[i] != '\t':
            inp_str += list_of_symbols[i]
        
    # print("inp_str")
    # print(inp_str)
    # print("list_of_symbols")
    # print(list_of_symbols)
        
    return analyse_input(inp_str, list_of_symbols)
    
def has_duplicate_values(d):
    seen_values = set()  # A set to store unique values encountered

    for value in d.values():
        if value in seen_values:
            return True  # Found a duplicate value
        seen_values.add(value)

    return False  # No duplicate values found

def find_first_op(list_of_symbols):
    for symbol in list_of_symbols:
        if symbol in my_operations:
            return symbol
    return None

def analyse_input(inp_str, list_of_symbols):
    print("inp_str")
    print(inp_str)
    # print("list_of_symbols")
    # print(list_of_symbols)
    # print("inp_str")
    # print(inp_str)
    copy_list = list_of_symbols
    
    first_found = str(find_first_op(copy_list))
    
    # print(str('lambda'))
        
    if first_found == '++':
        
    # if first_found == str('++'):
        return function_concat(inp_str)
    
    # elif first_found == str('+'):
    elif first_found == '+':
        
        return function_plus(inp_str)
    
    elif 'lambda' in inp_str:
        return function_lambda(inp_str, list_of_symbols)
        
    else:
        # print("no op")
        return no_opperations(inp_str)

def function_plus(inp_str):
    inp_str = re.sub(r'\s*\+\s*', ' ', inp_str)
    inp_str = inp_str.replace('(', '')
    inp_str = inp_str.replace(')', '')
    inp_str = inp_str.replace(' ', '')
    inp_str = inp_str.replace('\n', '')
    sum = 0
    for i in range(len(inp_str)):
        sum += int(inp_str[i])
    return(sum)

def function_concat(inp_str):
    inp_str = re.sub(r'\s*\+\+\s*', ' ', inp_str)
    nested_lists = parse_nested_list(inp_str)
    
    flag = True
    
    for i in range(len(nested_lists[0])):
        if nested_lists[0][i] == []:
            flag = False

    flattened_list = recursive_concat(nested_lists, flag)
    str_list = [str(i) for i in flattened_list]

    result = '( ' + ' '.join(str_list) + ' )'
    # result = re.sub(r'\s*\[\s*', '(', result)
    result = result.replace('[', '(')
    result = result.replace(']', ')')
    return result

        
def recursive_concat(list_of_lists, preserve_empty):
    if not list_of_lists:
        return []
    
    if isinstance(list_of_lists[0], list):
        head = recursive_concat(list_of_lists[0], preserve_empty)
        if preserve_empty and not head and list_of_lists[0] == []:
            head = [[]]
        return head + recursive_concat(list_of_lists[1:], preserve_empty)
    else:
        return [list_of_lists[0]] + recursive_concat(list_of_lists[1:], preserve_empty)
    
def no_opperations(inp_str):
    if len(inp_str) == 1:
        return inp_str
    if '()' in inp_str:
        inp_str = inp_str.replace('(  )', '()')
        # print("ce am objcccccccht")
    else:         
        if ') (' in inp_str:
            inp_str = inp_str.replace(') (', ' ')
    nested_lists = parse_nested_list(inp_str)
    
    str_list = [str(i) for i in nested_lists]
    
    result = '( ' + ' '.join(str_list) + ' )'
    result = result.replace(',', '')
    
    result = result.replace('[', '( ')
    result = result.replace(']', ' )')
    
    if '(  )' in result:
        result = result.replace('(  )', '()')
    
    return result

def remove_nested_parentheses(s):
    while "( (" in s and ") )" in s:
        s = s.replace("( (", "(", 1)  # Replace first occurrence of '( ('
        s = s.replace(") )", ")", 1)  # Replace first occurrence of ') )'
    return s

def remove_parentheses(nested_list, x):
    def unwrap(lst, depth):
        if depth > 0 and isinstance(lst, list):
            if lst:  # Check if list is not empty
                return unwrap(lst[0], depth - 1)
            else:
                return lst  # Return the empty list if encountered
        return lst

    return unwrap(unwrap(nested_list, x), -x)

def no_of_lambdas(list_of_symbols):
    no_lambda = 0
    for i in range(len(list_of_symbols)):
        if list_of_symbols[i] == 'lambda':
            no_lambda += 1
    return no_lambda


def function_lambda(expr, list_of_symbols):
    # print("ana")
    no_lambda = no_of_lambdas(list_of_symbols)
    # print("no_lambda")
    vect_of_remains = []
    amobt = my_parse_expression(expr, no_lambda, vect_of_remains)
    rez_fin = amobt[0]
    vect_of_remains = amobt[1]
    
    

    evaluated_expr = evaluate_expression(parse_expression(rez_fin), vect_of_remains, no_lambda, 1)
    # evaluated_expr = remove_parentheses(evaluated_expr, no_lambda + 1)

    no_paran = no_lambda 
    my_rez = str(evaluated_expr)
    
    my_rez = my_rez[no_paran:-no_paran]
   
    
    my_lambdas = []
    
    contor = 1
    for i in range(no_lambda):
        my_lambdas.append(expr[contor])
        contor += 2
    
    
    result = str(my_rez)
    result = result.replace(',', '')
    result = result.replace('[', '(')
    result = result.replace(']', ')')
    

    if check_on_res(result)[0] == True:
        result = result[1:-1]
        
    # print("result ha")
    # print(result)
    # print("fi")
    # print(fi)
    # print("list_of_symbols")
    # print(list_of_symbols)
    # list_of_symbols.remove(fi)
    # print("list_of_symbols")
    # print(list_of_symbols)
    
    return analyse_input(result, list_of_symbols)

def count_start_end_parentheses(s):
    start_count = 0
    end_count = 0
    s = s.replace(" ", "")
    # Count the opening parentheses at the start
    for char in s:
        if char == '(':
            start_count += 1
        else:
            break  # Stop counting when a non-opening parenthesis character is encountered

    # Count the closing parentheses at the end
    for char in reversed(s):
        if char == ')':
            end_count += 1
        else:
            break  # Stop counting when a non-closing parenthesis character is encountered

    return start_count, end_count
  
def check_on_res(res):
    # print("res")
    # print(res)
    start_count, end_count = count_start_end_parentheses(res)
    # print("start_count")
    # print(start_count)
    if start_count == end_count and start_count % 2 == 1:
        return True, start_count
    else:
        return False, start_count
    
def parse_expression(expr):
    # This is a very basic parser and needs to be expanded
    # to handle more complex expressions properly
    expr = expr.replace("(", " ( ").replace(")", " ) ").split()

    def parse(tokens):
        if not tokens:
            raise SyntaxError("Unexpected EOF")

        token = tokens.pop(0)
        if token == '(':
            new_list = []
            while tokens[0] != ')':
                new_list.append(parse(tokens))
            tokens.pop(0)  # remove ')'
            return new_list
        elif token == ')':
            raise SyntaxError("Unexpected )")
        else:
            try:
                return int(token)
            except ValueError:
                return str(token)

    return parse(expr)


def my_parse_expression(expr, no_lambda, vect_of_remains):
    #  initial : "(((lambda x: lambda y: lambda z: x 1) 2) 3)"
    
    if no_lambda == 1:
        return expr, vect_of_remains
    parsed_expr = parse_expression(expr)
    
    new_expr = str(parsed_expr[0])
    vect_of_remains.append(parsed_expr[1])
    new_expr = new_expr.replace("[", "(")
    new_expr = new_expr.replace("]", ")")
    new_expr = new_expr.replace(",", "")
    new_expr = new_expr.replace("'", "")
    
    return my_parse_expression(new_expr, no_lambda - 1, vect_of_remains)


def evaluate_expression(expr, vect_of_remains, no_lambda, val):
    
    
    my_dim = 2 * no_lambda

    my_rez = []
    my_lambdas = []
    
    contor = 1
    for i in range(no_lambda):
        my_lambdas.append(expr[contor])
        contor += 2
    
    
    
    my_lambdas_cont = dict()
    
    contor = 1
    for i in range(no_lambda):
        my_lambdas.append(expr[contor])
        my_lambdas_cont[contor] = expr[contor]
        contor += 2
    
    
    if has_duplicate_values(my_lambdas_cont):
        
        calc = 1
        expr[calc] = str('y:')
        
    # print("expr dupa ce am facut calc")
    # print(expr)
    # print("------------------")


    my_rule = expr[my_dim]
    # print("my_rule")
    # print(my_rule)
    if not isinstance(my_rule, list):
        my_rule = [my_rule]
    
    my_op = ''
    new_dict = []
    new_dict = my_rule
    
    len_rule = len(my_rule)
    
   

    for i in range(len_rule):
        for j in range(no_lambda):
            index_lambda = str(my_lambdas[0])
            index_lambda = index_lambda.replace(":", "")
            
            
            if my_rule[i] == index_lambda:
                my_list = [expr[len(expr) - 1]]
                new_dict[i] = my_list
            elif has_duplicate_values(my_lambdas_cont):
                new_dict[i] = index_lambda
 
    
    for i in range(2, my_dim):
        my_rez.append(expr[i])
    my_rez.append(new_dict)
    if len(vect_of_remains) - val >= 0:
        my_rez.append(vect_of_remains[len(vect_of_remains) - val])
    val += 1
    
    if no_lambda == 1:

        return my_rez
    else:
        return evaluate_expression(my_rez, vect_of_remains, no_lambda - 1, val)


def parse_nested_list(s):
    def nest(tokens):
        res = []
        while tokens:
            token = tokens.pop(0)
            if token == '(':
                res.append(nest(tokens))
            elif token == ')':
                return res
            else:
                res.append(int(token))
        return res

    tokens = s.replace('(', ' ( ').replace(')', ' ) ').split()
    
    return nest(tokens)[0]



if __name__ == '__main__':
    main()
