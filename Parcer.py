import math

class Parcer:
    
    sin = ['sin', 'cos', 'tan', 'ctn', 'log']
    sin_shorts = ['s', 'c', 't', 'g', 'l']
    
    def _eval(expression: str, x):
        if expression.count('(') == 0 and expression.count('[') == 0 and expression.count('$') == 0:
            return eval(expression)
        
        for old, new in zip(Parcer.sin, Parcer.sin_shorts):
            expression = expression.replace(old, new)
            
        return Parcer.calculate(expression, x)
    
    
    def getAbs(res: str):
        i = str(res)
        i = int(eval(i[1:-1]))
        return str(abs(i))
    
    def getX(res: str, x):
        return res.replace('${}$'.format(str(x)), '({})'.format(str(x)))

    def getSin(i, s = None):
        if s == 's':
            return math.sin(i)
        elif s == 'c':
            return math.cos(i)
        elif s == 't':
            return math.tan(i)
        elif s == 'g':
            return 1/math.tan(i)
        elif s == 'l':
            try:
                return math.log10(i)
            except ValueError:
                return None
        else:
            return i
        
        
    def calculate(expression: str, x: str):
        
        if expression.count('(') == 0 and expression.count('[') == 0 and expression.count('$') == 0:
            try:
                return eval(expression)
            except TypeError:
                return
        
        res = ''
        state = ''
        able = True
        for l in expression:
            #check sin
            if l in Parcer.sin_shorts:
                state = l
                continue
            #find the smallest
            if l == '(' and able or l == '[' and able:
                res = ''
                res += l
               
            #start 
            elif l == '(' or l == '[':
                able = True
                res += l
                
            elif able:
                res += l

            #end
            if l == ')' and able or l == ']' and able:
                break
        
        original_res = str(res)
        if '[' in res: 
            res = Parcer.getAbs(res)
            if state != '':
                original_res = '({})'.format(original_res)
        
        new = Parcer.getX(res, x)
        new = Parcer.getSin(eval(new), state)
        expression = expression.replace(state + original_res, str(new))
        return Parcer.calculate(expression, x)
        
        
                
            