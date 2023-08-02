from typing import Any


class BaseParser:
    __slots__ = (
        'code',
        'ast',
        'not_close_block'
    )

    def __init__(self, code: str) -> None:
        self.code: str = code
        self.ast: dict = {}
        self.not_close_block: list = []

    def getNestedBlock(self):
        if self.not_close_block:
            block = self.ast
            for name in self.not_close_block:
                block = block[name]['block']

            return block

        else:
            return self.ast

    def parsing(self) -> Any:
        ...


class Use(BaseParser):
    __slots__ = BaseParser.__slots__

    def parsing(self) -> dict:
        _, module_name = self.code.split()
        return module_name


class Function(BaseParser):
    __slots__ = BaseParser.__slots__
    id = 0

    def parsing(self):
        code = ' '.join(self.code.split()).removeprefix('func')
        opening_brace, closing_brace = (
            code.index('('),
            code.index(')')
        )
        function_name = code[:opening_brace].split()[0]
        function_args = code[opening_brace + 1:closing_brace]
        self.ast[function_name] = {
            'type': 'function',
            'args': function_args,
            'block': {

            }
        }
        return (
            function_name,
            self.ast,
            code[code.index('{') + 1:]
        )


class Condition(BaseParser):
    __slots__ = ('conds', ) + BaseParser.__slots__
    id = 0

    def parsing(self):
        cond_name = f'coundition_{Condition.id}'
        self.ast[cond_name] = {
            'block': {

            }
        }
        code = self.code[:self.code.index('{')]
        self.ast[cond_name]['conds'] = self.condParsing(
            code[code.index('(') + 1:code.rfind(')') - 1]
        )
        Condition.id += 1
        return (
            cond_name,
            self.ast,
            self.code[self.code.find('{') + 1:]
        )

    def condParsing(self, code):
        conds = code.split(' and ')
        if len(conds) > 1:
            return (
                'and',
                [self.condParsing(cond) for cond in conds]
            )

        else:
            conds = code.split(' or ')
            if len(conds) > 1:
                return (
                    'or',
                    [self.condParsing(cond) for cond in conds]
                )

            else:
                return (None, code)


class Variable(BaseParser):
    __slots__ = BaseParser.__slots__

    def parsing(self) -> Any:
        var_name = self.code[:self.code.index('=')].split()[0]
        var_value = self.code[self.code.index('=') + 1:]
        if '"' in var_value:
            var_value = var_value[
                        var_value.index('"'):
                        var_value.rfind('"') + 1]
        elif "'" in var_value:
            var_value = var_value[
                        var_value.index("'"):
                        var_value.rfind("'") + 1]
        else:
            var_value = var_value.split()[0]

        self.ast[var_name] = {
            'value': var_value,
            'type': 'string'
                    if (var_value[0], var_value[-1]) == ('"', '"') or
                       (var_value[0], var_value[-1]) == ("'", "'") else 'int'
        }
        return self.ast


class Loop(BaseParser):
    __slots__ = BaseParser.__slots__
    id = 0

    def parsing(self):
        code = self.code.removeprefix(' loop ')
        loop_name = f'loop_{Loop.id}'
        Loop.id += 1
        self.ast[loop_name] = {
            'block': {

            }
        }
        return (
            loop_name,
            self.ast,
            code[code.index('{') + 1:]
        )


class Parser(BaseParser):
    __slots__ = BaseParser.__slots__

    def codeRefactor(self) -> list[str, ...]:
        return (
            ' '.join(self.code.split())
            .replace('{', ' { ')
            .replace('}', '};')
            .replace('(', ' ( ')
            .replace(')', ' ) ')
            .replace('==', ' == ')
            .replace('!=', ' != ')
            .replace('<=', ' <= ')
            .replace('>=', ' >= ')
        ).split(';')

    def parsing(self, code: str):
        _code_: list = code.split()
        if not _code_: return

        block: dict = self.getNestedBlock()
        match _code_[0]:
            case 'use':
                useParser = Use(code)
                module_name = useParser.parsing()
                block.setdefault('using', set()).add(module_name)

            case 'func':
                functionParser = Function(code)
                fn_name, ast, code = functionParser.parsing()
                self.not_close_block.append(fn_name)
                block.update(ast)
                self.parsing(code)

            case 'loop':
                loopParser = Loop(code)
                loop_name, ast, code = loopParser.parsing()
                self.not_close_block.append(loop_name)
                block.update(ast)
                self.parsing(code)

            case 'if':
                condParser = Condition(code)
                cond_name, ast, code = condParser.parsing()
                self.not_close_block.append(cond_name,)
                block.update(ast)
                self.parsing(code)

            case '}':
                try:
                    self.not_close_block.pop()
                except IndexError:
                    pass

            case _:
                if '=' in code:
                    varParser = Variable(code)
                    block.update(varParser.parsing())

    def run(self) -> dict:
        revisedСode: list[str, ...] = self.codeRefactor()
        for code in revisedСode:
            self.parsing(code)


        print(printDict(self.ast))


def printDict(d: dict, indent=''):
    string = '{\n'
    for key, value in d.items():
        if isinstance(value, dict):
            value = printDict(value, indent='  ' + indent)

        string += f'  {indent}{key}: {value}\n'

    return string + f'{indent}}}'
