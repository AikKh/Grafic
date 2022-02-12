import random
folmulas = {'Constant function': '6',
            'Linear function': 'x',
            'Quadratic function': 'x**2',
            'Cubic function': 'x**3',
            '': ''}

if __name__ == '__main__':
    for i in range(10):
        print(random.randrange(11), end=', ')
    