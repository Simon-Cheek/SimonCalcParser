from pair import *
from operator import add, sub, mul, truediv


def tokenize(expression):
    input_string = expression
    edit1 = input_string.replace('(', '( ')
    edit2 = edit1.replace(')', ' )')
    input_list = edit2.split()
    return input_list


def parse_tokens(tokens, index):
    operator = None
    if tokens[index] == '(':
        operator = tokens[index + 1]
        if index != 0:
            nest, new_index = parse_tokens(tokens, index + 2)
            index = new_index
            operator = Pair(operator, nest)
        if index == 0:
            index += 2
        new_nest, new_index = parse_tokens(tokens, index)
        index = new_index
        return Pair(operator, new_nest), index
    if tokens[index] == ')':
        return nil, index + 1
    try:
        num_token = None
        if '.' in tokens[index]:
            num_token = float(tokens[index])
        elif '.' not in tokens[index]:
            num_token = int(tokens[index])
        new_list, new_index = parse_tokens(tokens, index + 1)
        index = new_index
        return Pair(num_token, new_list), index
    except ValueError:
        raise TypeError('That\'s not right')


def parse(tokens):
    pair_object, final_index = parse_tokens(tokens, 0)
    return pair_object


def reduce(func, operands, initial):
    total = initial
    while True:
        if operands is nil:
            break
        total = func(total, operands.first)
        operands = operands.rest
    return total


def apply(operator, operands):
    if operator == '+':
        answer = reduce(add, operands, 0)
    elif operator == '-':
        answer = reduce(sub, operands.rest, operands.first)
    elif operator == '*':
        answer = reduce(mul, operands, 1)
    elif operator == '/':
        answer = reduce(truediv, operands.rest, operands.first)
    else:
        raise TypeError('Oh please!')
    return answer


def eval(tree):
    if isinstance(tree, int):
        return tree
    if isinstance(tree, float):
        return tree
    if isinstance(tree, Pair):
        if isinstance(tree.first, Pair):
            subtree = eval(tree.first)
            rest_of_tree = tree.rest.map(eval)
            return Pair(subtree, rest_of_tree)
        else:
            subtree = tree.rest.map(eval)
            return apply(tree.first, subtree)
    else:
        raise TypeError('So close')


def main():
    print('Welcome to the CS 111 Calculator Interpreter.')
    # the main loop FOLLOWS the greeting
    while True:
        var = input('calc >> ')
        if var == 'exit':
            break
        tokens = tokenize(var)
        try:
            pair_object = parse(tokens)
            final_val = eval(pair_object)
            print(final_val)
        except TypeError:
            print(TypeError)
    print('Goodbye!')


if __name__ == "__main__":
    main()

