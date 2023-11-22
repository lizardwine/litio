import argparse
import importlib.util
import os
import rich
import yaml

__version__ = '1.0.0.2'

class Args:
    def __init__(self, args):
        for key, value in args.items():
            setattr(self, key, value)

def params_to_dic(params: list) -> dict:
    dict_params = {}
    for i in range(0,len(params),2):
        param = {params[i]:params[i+1]}
        dict_params.update(param)

    return dict_params
def eval_params_values(params: dict,functions: dict) -> dict:
    for key,value in params.items():
        if functions[key] in [int,float]:
            params[key] = functions[key](value)
        elif functions[key] != str:
            params[key] = eval(value)
        else:
            params[key] = f'{value}'
    return params
def Main(args):
        module_name = 'module'
        spec = importlib.util.spec_from_file_location(module_name, args.file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if "." in args.function:
            _class = getattr(module,args.function.split(".")[0])
            function = _class.__dict__[args.function.split(".")[1]]
            if type(function) == classmethod:
                function_type = "classmethod"
            else:
                function_type = "method"
            function_params = function.__annotations__
        else:
            function_type = "function"
            function_params = getattr(module,args.function).__annotations__
            
        if type(args.params) == list:    
            params = params_to_dic(args.params)
            params = eval_params_values(params,function_params)
        else:
            params = args.params
        return_value = None
        to_return = None
        to_return_assert = None
        if function_type == "method":
            init_params = getattr(module,args.function.split('.')[0]).__init__.__annotations__
            if type(args.instance_params) == list:    
                instance_params = params_to_dic(args.instance_params)
                instance_params = eval_params_values(instance_params,init_params)
            else:
                instance_params = args.instance_params
        try:
            if function_type == "function":
                fun = getattr(module,args.function)
                if args.print_return:
                    return_value = fun(**params)
                    to_return = (return_value)
                else:
                    return_value = fun(**params)
            elif function_type == "method":
                class_name = args.function.split(".")[0]
                method_name = ".".join(args.function.split(".")[1:])
                _class = getattr(module,class_name)
                instance = _class(**instance_params)
                if args.print_return:
                    return_value = getattr(instance,method_name)(**params)
                    to_return = (return_value)
                else:
                    return_value = getattr(instance,method_name)(**params)
            elif function_type == "classmethod":
                if args.print_return:
                    _class = getattr(module,args.function.split(".")[0])
                    fun = getattr(_class,args.function.split(".")[1])
                    return_value = fun(**params)
                    to_return = (return_value)
                else:
                    _class = getattr(module,args.function.split(".")[0])
                    fun = getattr(_class,args.function.split(".")[1])
                    return_value = fun(**params)
        
            if args.assertion != None:
                if args.assert_to == None:
                    to_return_assert = ('No assertion to perform')
                if args.assertion == "Equals":
                    to_return_assert = (return_value == args.assert_to)
                elif args.assertion == "NotEquals":
                    to_return_assert = (return_value != args.assert_to)
                elif args.assertion == "Greater":
                    to_return_assert = (return_value > float(args.assert_to))
                elif args.assertion == "GreaterOrEquals":
                    to_return_assert = (return_value >= float(args.assert_to))
                elif args.assertion == "Less":
                    to_return_assert = (return_value < float(args.assert_to))
                elif args.assertion == "LessOrEquals":
                    to_return_assert = (return_value <= float(args.assert_to))
                elif args.assertion == "In":
                    to_return_assert = (return_value in eval(args.assert_to))
                elif args.assertion == "NotIn":
                    to_return_assert = (return_value not in eval(args.assert_to))
                elif args.assertion == "Is":
                    to_return_assert = (return_value is eval(args.assert_to))
                elif args.assertion == "IsNot":
                    to_return_assert = (return_value is not eval(args.assert_to))
                elif args.assertion == "IsNone":
                    to_return_assert = (return_value is None)
                elif args.assertion == "IsNotNone":
                    to_return_assert = (return_value is not None)
                elif args.assertion == "IsInstance":
                    to_return_assert = (return_value.__class__ == getattr(module,args.assert_to))
                elif args.assertion == "IsNotInstance":
                    to_return_assert = (return_value.__class__ != getattr(module,args.assert_to))
            return [to_return,to_return_assert]
        except Exception as e:
            return to_return, False

def litio():
    parser = argparse.ArgumentParser(description='A command line function tester')
    parser.add_argument('--version','-v',action='version',version='%(prog)s {}'.format(__version__))
    parser.add_argument('--config-file','-c',dest="config_file",help='config file',required=False, default="litio.yml")
    parser.add_argument('--verbose', '-V', dest="verbose", help="enable verbosity", required=False, action=argparse.BooleanOptionalAction)


    args = parser.parse_args()

    if not os.path.exists(args.config_file):
        rich.print(f"[bold red]Config file \"[bold yellow]{args.config_file}[/bold yellow]\" does not exist[/bold red]")
        exit(1)
    data = open(args.config_file,'r').read()
    data = yaml.safe_load(data)
    rich.print(f"[bold cyan]{data.get('name')}[/bold cyan]")
    tests_passed = []
    failed_tests = []
    for test, test_data in data["tests"].items():
        path = test_data['path']
        rich.print(f"   - [bold blue]{test} - {path}[/bold blue]")
        for function in test_data['functions']:
            function_name = list(function.keys())[0]
            rich.print(f"       - [bold magenta]{function_name}[/bold magenta]")
            inputs = eval(str(function[function_name]["inputs"]))
            argsDitctionary = {
                "file": path,
                "function": function_name,
                "params": function[function_name]["inputs"],
            }
            if function[function_name].get('expected'):
                argsDitctionary.update({"assertion":function[function_name]["expected"]["comparator"], "assert_to":function[function_name]["expected"]["value"]})
            if function[function_name].get('instance'):
                argsDitctionary.update({"instance_params":function[function_name]["instance"]})
            if not function[function_name].get('print-return'):
                argsDitctionary.update({"print_return":False or args.verbose})
            else:
                argsDitctionary.update({"print_return":function[function_name]["print-return"] or args.verbose})
            argsToMain = Args(argsDitctionary)
            to_print, assertion = Main(argsToMain)
            if args.verbose:
                rich.print(f"[bold yellow]           -  inputs:[/bold yellow]")
                for key, value in inputs.items():
                    rich.print(f"[bold yellow]               -  {key}: {value}[/bold yellow]")
                rich.print(f"[bold yellow]           -  assertion: {argsToMain.assertion}[/bold yellow]")
                argsToMain.assert_to = f"'{argsToMain.assert_to}'" if type(argsToMain.assert_to) == str else argsToMain.assert_to
                rich.print(f"[bold yellow]           -  assert to: {argsToMain.assert_to}[/bold yellow]")
                
            if argsToMain.print_return or args.verbose:
                to_print = f"'{to_print}'" if type(to_print) == str else to_print
                rich.print(f"[bold yellow]           -  returned: {to_print}[/bold yellow]")
            if assertion:
                rich.print(f"[bold green]           -  Test: passed[/bold green]")
                tests_passed.append(True)
            else:
                rich.print(f"[bold red]           -  Test: failed[/bold red]")
                tests_passed.append(False)
                failed_tests.append({
                    "name": test,
                    "file": path,
                    "function_name": function_name,
                    "inputs": inputs,
                    "assertion": argsToMain.assertion,
                    "assert_to": argsToMain.assert_to,
                    "returned": to_print
                })
    if all(tests_passed):
        rich.print(f"[bold green]{len(tests_passed)}/{len(tests_passed)} tests passed[/bold green]")
    else:
        if True in tests_passed:
            rich.print(f"[bold yellow]{tests_passed.count(True)}/{len(tests_passed)} tests passed[/bold yellow]")
            rich.print("[bold red]Failed tests:[/bold red]")
            prev_path = None # var to keep track of the previous path
            for test in failed_tests:
                if test['file'] != prev_path:
                    rich.print(f"[bold blue]   - {test['name']} - {test['file']}[/bold blue]")
                    prev_path = test['file']
                rich.print(f"[bold magenta]       - {test['function_name']}[/bold magenta]")
                rich.print(f"[bold yellow]           - inputs:[/bold yellow]")
                for key, value in test['inputs'].items():
                    rich.print(f"[bold yellow]             - {key}: {value}[/bold yellow]")
                rich.print(f"[bold yellow]           - assertion: {test['assertion']}[/bold yellow]")
                rich.print(f"[bold yellow]           - assert to: {test['assert_to']}[/bold yellow]")
                rich.print(f"[bold yellow]           - returned: {test['returned']}[/bold yellow]")    
        else:
            rich.print(f"[bold red]0/{len(tests_passed)} tests passed[/bold red]")
        
    exit(0)

if __name__ == '__main__':
    litio()
