import sys
import importlib
import inspect
import ast
import textwrap
import difflib

def rec_inspect(module, name):
    res = []
    for member in inspect.getmembers(module):
        if not member[0].startswith('__') and not inspect.ismodule(member[1]):
            if inspect.isfunction(member[1]):
                res.append((name + '.' + member[0], textwrap.dedent(inspect.getsource(member[1]))))
            elif inspect.isclass(member[1]):
                res.extend(rec_inspect(member[1], name + '.' + member[0]))
        elif inspect.isfunction(member[1]):
            res.append((name + '.' + member[0], textwrap.dedent(inspect.getsource(member[1]))))
    return res


mod_funs = []

for arg in sys.argv[1:]:
    module = importlib.import_module(arg)
    mod_funs.extend(rec_inspect(module, arg))

clear_funs = []

for fun in mod_funs:
    tmp = ast.parse(fun[1])
    for node in ast.walk(tmp):
        for s in ('name', 'id', 'arg', 'attr'):
            node.__setattr__(s, '_')
    clear_funs.append((fun[0], ast.unparse(tmp)))

l = len(clear_funs)
for i in range(l):
    for j in range(i+1, l):
        if difflib.SequenceMatcher(None, clear_funs[i][1], clear_funs[j][1]).ratio() > 0.95:
            print(clear_funs[i][0], " : ", clear_funs[j][0])
