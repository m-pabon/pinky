from tokens import Token

class Node:
    '''
    The parent class of every node in the ast
    '''
    pass


class Expr(Node):
    '''
    Evaluate to a result
    '''
    pass

class Stmt(Node):
    '''
    Perform an action
    '''
    pass

class Decl(Stmt):
    pass

class Integer(Expr):
    def __init__(self, value, line):
        assert isinstance(value, int), value
        self.value = value
        self.line = line
    def __repr__(self):
        return f'Integer[{self.value}]'

class Float(Expr):
    def __init__(self, value, line):
        assert isinstance(value, float), value
        self.value = value
        self.line = line
    def __repr__(self):
        return f'Float[{self.value}]'

class Bool(Expr):
    def __init__(self, value, line):
        assert isinstance(value, bool), value
        self.value = value
        self.line = line
    def __repr__(self):
        return f'Bool[{self.value}]'
    
class String(Expr):
    def __init__(self, value, line):
        assert isinstance(value, str), value
        self.value = value
        self.line = line
    def __repr__(self):
        return f'String[{self.value}]'

class UnOp(Expr):
    def __init__(self, op: Token, operand: Expr, line):
        assert isinstance(op, Token), op
        assert isinstance(operand, Expr), operand
        self.op = op
        self.operand = operand
        self.line = line
    def __repr__(self):
        return f'UnOp({self.op.lexeme}, {self.operand})'

class BinOp(Expr):
    def __init__(self, op: Token, left: Expr, right: Expr, line):
        assert isinstance(op, Token), op
        assert isinstance(left, Expr), left
        assert isinstance(right, Expr), right
        self.op = op
        self.left = left
        self.right = right
        self.line = line
    def __repr__(self):
        return f'BinOp({self.op.lexeme}, {self.left}, {self.right})'

class LogicalOp(Expr):
    def __init__(self, op: Token, left: Expr, right: Expr, line):
        assert isinstance(op, Token), op
        assert isinstance(left, Expr), left
        assert isinstance(right, Expr), right
        self.op = op
        self.left = left
        self.right = right
        self.line = line
    def __repr__(self):
        return f'LogicalOp({self.op.lexeme}, {self.left}, {self.right})'

class Grouping(Expr):
    def __init__(self, value: Expr, line):
        assert isinstance(value, Expr), value
        self.value = value
        self.line = line
    def __repr__(self):
        return f'Grouping({self.value})'

class Identifier(Expr):
    def __init__(self, name, line):
        self.name = name
        self.line = line
    def __repr__(self):
        return f'Identifier[{self.name}]'

class Stmts(Node):
    '''
    A list of statements
    '''
    def __init__(self, stmts, line):
        assert all(isinstance(stmt, Stmt) for stmt in stmts), stmts
        self.stmts = stmts
        self.line = line
    def __repr__(self):
        return f'Stmts({self.stmts})'

class PrintStmt(Stmt):
    def __init__(self, value, end, line):
        assert isinstance(value, Expr), value
        self.value = value
        self.end = end
        self.line = line
    def __repr__(self):
        return f'PrintStmt({self.value}, end={self.end!r})'

class IfStmt(Stmt):
    '''
    "if" <expr> "then" <then_stmts> ("else" <else_stmts>)? "end"
    '''
    def __init__(self, test, then_stmts, else_stmts, line):
        assert isinstance(test, Expr), test
        assert isinstance(then_stmts, Stmts), then_stmts
        assert else_stmts is None or isinstance(else_stmts, Stmts), else_stmts
        self.test = test
        self.then_stmts = then_stmts
        self.else_stmts = else_stmts
        self.line = line
    def __repr__(self):
        return f'IfStmt({self.test}, then:{self.then_stmts}, else:{self.else_stmts})'

class WhileStmt(Stmt):
    def __init__(self, test, stmts, line):
        assert isinstance(test, Expr), test
        assert isinstance(stmts, Stmts), stmts
        self.test = test
        self.stmts = stmts
        self.line = line
    def __repr__(self):
        return f'WhileStmt({self.test}, stmts:{self.stmts})'
        
class LocalAssignment(Stmt):    
    def __init__(self, left, right, line):
        assert isinstance(left, Expr), left
        assert isinstance(right, Expr), right
        self.left = left
        self.right = right
        self.line = line
    def __repr__(self):
        return f'LocalAssignment({self.left}, {self.right})'

class Assignment(Stmt):
    def __init__(self, left, right, line):
        assert isinstance(left, Expr), left
        assert isinstance(right, Expr), right
        self.left = left
        self.right = right
        self.line = line
    def __repr__(self):
        return f'Assignment({self.left}, {self.right})'

class ForStmt(Stmt):
    def __init__(self, ident, start, end, step, stmts, line):
        assert isinstance(ident, Identifier), ident
        assert isinstance(start, Expr), start
        assert isinstance(end, Expr), end
        assert isinstance(step, Expr) or step is None, step
        assert isinstance(stmts, Stmts), stmts
        self.ident = ident
        self.start = start
        self.end = end
        self.step = step
        self.stmts = stmts
        self.line = line
    def __repr__(self):
        return f'ForStmt({self.ident}, {self.start}, {self.end}, {self.step}, {self.stmts})'

class FuncDecl(Decl):
    def __init__(self, name, params, stmts, line):
        assert isinstance(name, str), name
        assert all(isinstance(param, Param) for param in params), params
        self.name = name
        self.params = params
        self.stmts = stmts
        self.line = line
    def __repr__(self):
        return f'FuncDecl({self.name!r}, {self.params}, {self.stmts})'

class Param(Decl):
    def __init__(self, name, line):
        assert isinstance(name, str), name
        self.name = name
        self.line = line
    def __repr__(self):
        return f'Param[{self.name!r}]'

class FuncCall(Expr):
    def __init__(self, name, args, line):
        self.name = name
        self.args = args
        self.line = line
    def __repr__(self):
        return f'FuncCall({self.name!r}, {self.args})'

class FuncCallStmt(Stmt):
    '''
    A special type of statement used to wrap FuncCall Expressions
    '''
    def __init__(self, expr):
        assert isinstance(expr, FuncCall), expr
        self.expr = expr
    def __repr__(self):
        return f'FuncCallStmt({self.expr})'

class RetStmt(Stmt):
    def __init__(self, value, line):
        self.value = value
        self.line = line
    def __repr__(self):
        return f'RetStmt[{self.value}]'
