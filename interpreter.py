from model import *
from tokens import *
from utils import *
from state import *
from defs import *

import codecs

class Interpreter:
    def interpret(self, node, env):
        if isinstance(node, Integer):
            return (TYPE_NUMBER, float(node.value))
        elif isinstance(node, Float):
            return (TYPE_NUMBER, float(node.value))
        elif isinstance(node, Bool):
            return (TYPE_BOOL, node.value)
        elif isinstance(node, String):
            return (TYPE_STRING, node.value)
        elif isinstance(node, Grouping):
            return self.interpret(node.value, env)
        elif isinstance(node, Identifier):
            value = env.get_var(node.name)
            if value is None:
                runtime_error(f'Undeclared Identifier({node.name!r})', node.line)
            if value[1] is None:
                runtime_error(f'Uninitialized Identifier({node.name!r})', node.line)
            return value
        elif isinstance(node, Assignment):
            righttype, rightval = self.interpret(node.right, env)
            env.set_var(node.left.name, (righttype, rightval))
        elif isinstance(node, LocalAssignment):
            righttype, rightval = self.interpret(node.right, env)
            env.set_local(node.left.name, (righttype, rightval)) 
        elif isinstance(node, BinOp):
            lefttype, leftval = self.interpret(node.left, env)
            righttype, rightval = self.interpret(node.right, env)
            if node.op.token_type == TOK_PLUS:
                if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
                    return (TYPE_NUMBER, leftval + rightval)
                elif lefttype == TYPE_STRING or righttype == TYPE_STRING:
                    return (TYPE_STRING, stringify(leftval) + stringify(rightval))
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme} between {lefttype} and {righttype}.', node.op.line)
            elif node.op.token_type == TOK_MINUS:
                if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
                    return (TYPE_NUMBER, leftval - rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme} between {lefttype} and {righttype}.', node.op.line)
            elif node.op.token_type == TOK_STAR:
                if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
                    return (TYPE_NUMBER, leftval * rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme} between {lefttype} and {righttype}.', node.op.line)
            elif node.op.token_type == TOK_SLASH:
                if rightval == 0:
                    runtime_error(f'Division by zero.', node.line)
                if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
                    return (TYPE_NUMBER, leftval / rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme} between {lefttype} and {righttype}.', node.op.line)
            elif node.op.token_type == TOK_MOD:
                if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
                    return (TYPE_NUMBER, leftval % rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme} between {lefttype} and {righttype}.', node.op.line)
            elif node.op.token_type == TOK_CARET:
                if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
                    return (TYPE_NUMBER, leftval ** rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme} between {lefttype} and {righttype}.', node.op.line)
            elif node.op.token_type == TOK_LT:
                if (lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER) or (lefttype == TYPE_STRING and righttype == TYPE_STRING):
                    return (TYPE_BOOL, leftval < rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme} between {lefttype} and {righttype}.', node.op.line)
            elif node.op.token_type == TOK_LE:
                if (lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER) or (lefttype == TYPE_STRING and righttype == TYPE_STRING):
                    return (TYPE_BOOL, leftval <= rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme} between {lefttype} and {righttype}.', node.op.line)
            elif node.op.token_type == TOK_GT:
                if (lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER) or (lefttype == TYPE_STRING and righttype == TYPE_STRING):
                    return (TYPE_BOOL, leftval > rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme} between {lefttype} and {righttype}.', node.op.line)
            elif node.op.token_type == TOK_GE:
                if (lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER) or (lefttype == TYPE_STRING and righttype == TYPE_STRING):
                    return (TYPE_BOOL, leftval >= rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme} between {lefttype} and {righttype}.', node.op.line)
            elif node.op.token_type == TOK_EQEQ:
                if (lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER) or (lefttype == TYPE_STRING and righttype == TYPE_STRING) or (lefttype == TYPE_BOOL and righttype == TYPE_BOOL):
                    return (TYPE_BOOL, leftval == rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme} between {lefttype} and {righttype}.', node.op.line)
            elif node.op.token_type == TOK_NE:
                if (lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER) or (lefttype == TYPE_STRING and righttype == TYPE_STRING) or (lefttype == TYPE_BOOL and righttype == TYPE_BOOL):
                    return (TYPE_BOOL, leftval != rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme} between {lefttype} and {righttype}.', node.op.line)

        elif isinstance(node, UnOp):
            operandtype, operandvalue = self.interpret(node.operand, env)
            if node.op.token_type == TOK_PLUS:
                if operandtype == TYPE_NUMBER:
                    return (TYPE_NUMBER, +operandvalue)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme} on {operandtype}.', node.op.line)
            elif node.op.token_type == TOK_MINUS:
                if operandtype == TYPE_NUMBER:
                    return (TYPE_NUMBER, -operandvalue)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme} on {operandtype}.', node.op.line)
            elif node.op.token_type == TOK_NOT:
                if operandtype == TYPE_BOOL:
                    return (TYPE_BOOL, not operandvalue)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme} on {operandtype}.', node.op.line)
        elif isinstance(node, LogicalOp):
            lefttype, leftval = self.interpret(node.left, env)
            if node.op.token_type == TOK_OR:
                if leftval:
                    return (lefttype, leftval)
            elif node.op.token_type == TOK_AND:
                if not leftval:
                    return(lefttype, leftval)
            return self.interpret(node.right, env)
        elif isinstance(node, Stmts):
            # Evaluate statments in sequence, one after another
            for stmt in node.stmts:
                self.interpret(stmt, env)
        elif isinstance(node, PrintStmt):
            exprtype, exprval = self.interpret(node.value, env)
            val = stringify(exprval)
            print(codecs.escape_decode(bytes(val, "utf-8"))[0].decode('utf-8'), end=node.end) #type: ignore
        elif isinstance(node, IfStmt):
            testtype, testval = self.interpret(node.test, env)
            if testtype != TYPE_BOOL:
                runtime_error("If Condition test is not a boolean expression.", node.line)
            if testval:
                self.interpret(node.then_stmts, env.new_env())
            else:
                self.interpret(node.else_stmts, env.new_env())
        elif isinstance(node, WhileStmt):
            testtype, testval = self.interpret(node.test, env)
            whileenv = env.new_env()
            if testtype != TYPE_BOOL:
                runtime_error("While Condition test is not a boolean expression.", node.line)
            if testval:
                while testval:
                    self.interpret(node.stmts, whileenv)
                    testval = self.interpret(node.test, env)[1]
        elif isinstance(node, ForStmt):
            varname = node.ident.name
            itype, i = self.interpret(node.start, env)
            endtype, end = self.interpret(node.end, env)
            block_new_env = env.new_env()
            if i < end:
                if node.step is None:
                    step = 1
                else:
                    steptype, step = self.interpret(node.step, env)
                while i <= end:
                    newval = (TYPE_NUMBER, i)
                    env.set_var(varname, newval)
                    self.interpret(node.stmts, block_new_env)
                    i = i + step
            else:
                if node.step is None:
                    step = -1
                else:
                    steptype, step = self.interpret(node.step, env)
                while i >= end:
                    newval = (TYPE_NUMBER, i)
                    env.set_var(varname, newval)
                    self.interpret(node.stmts, block_new_env)
                    i = i + step
        elif isinstance(node, FuncDecl):
            env.set_func(node.name, (node, env))
        elif isinstance(node, FuncCall):
            # 1. Make sure function was declared
            func = env.get_func(node.name)
            if not func:
                runtime_error(f'Function {node.name!r} not declared.', node.line)

            func_decl = func[0]
            func_env = func[1]

            # 2. Number of args matches
            if len(node.args) != len(func_decl.params):
                runtime_error(f'Function {func_decl.name!r} expected {len(func_decl.params)} params but {len(node.args)} arguments were passed.', node.line)
            # 3. Evaluate all the args
            args = []
            for arg in node.args:
                args.append(self.interpret(arg, env))
            # 4. Create local variables in child env of the func for the params and bind the args to them 
            new_func_env = func_env.new_env()
            for param, argval in zip(func_decl.params, args):
                new_func_env.set_local(param.name, argval)
            # 5. Interpret the body statements of the func decl
            try:
              self.interpret(func_decl.stmts, new_func_env)
            except Return as e:
              return e.args[0]
            
            
        elif isinstance(node, FuncCallStmt):
            self.interpret(node.expr, env)
        elif isinstance(node, RetStmt):
            raise Return(self.interpret(node.value, env))
    def interpret_ast(self, node):
        env = Environment()
        self.interpret(node, env)

class Return(Exception):
    pass
