import argparse
import os
import rich
import yaml
try:     
    from utils import ai, utils, tester
except ModuleNotFoundError:
    from .utils import ai, utils, tester

__version__ = '1.1.0.0'

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
            
            argsDitctionary = {
                "file": path,
                "function": function_name
            }
            if function[function_name].get('inputs'):
                inputs = eval(str(function[function_name]["inputs"]))
            else:
                inputs = {}
            argsDitctionary.update({"params":inputs})
            if function[function_name].get('expected'):
                argsDitctionary.update({"assertion":function[function_name]["expected"]["comparator"], "assert_to":function[function_name]["expected"]["value"]})
            if function[function_name].get('instance'):
                argsDitctionary.update({"instance_params":function[function_name]["instance"]})
            argsDitctionary.update({"print_return":function[function_name].get('print-return') or args.verbose or function[function_name].get('verbose')})
            argsToMain = utils.Args(argsDitctionary)
            
            main_response = tester.test(argsToMain)
            if not main_response:
                tests_passed.append(False)
                failed_tests.append({
                    'name': test,
                    'function_name': function_name,
                    'file': path,
                    'message': 'Function not found'
                })
                continue
            if isinstance(main_response, str) or not main_response[1]:
                fixed_bug = ai.fix_bug(function_name=function_name, path=path, data=data, inputs=inputs, main_response=main_response, function=function, args=args)
                if not fixed_bug:
                    failed_tests.append(False)
                    continue
                to_print = fixed_bug[0]
                assertion = fixed_bug[1]
            else:
                to_print = main_response[0]
                assertion = main_response[1]
            
            if args.verbose or function[function_name].get('verbose'):
                if inputs != {}:
                    rich.print(f"[bold yellow]           -  inputs:[/bold yellow]")
                    for key, value in inputs.items():
                        rich.print(f"[bold yellow]               - {key}: {value}[/bold yellow]")
                rich.print(f"[bold yellow]           -  assertion: {argsToMain.assertion}[/bold yellow]")
                argsToMain.assert_to = f"'{argsToMain.assert_to}'" if type(argsToMain.assert_to) == str else argsToMain.assert_to
                rich.print(f"[bold yellow]           -  assert to: {argsToMain.assert_to}[/bold yellow]")
                
            if argsToMain.print_return or args.verbose or function[function_name].get('verbose'):
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
                if test.get('message'):
                    rich.print(f"[bold red]           - message: {test['message']}[/bold red]")
                    continue
                if inputs != {}:
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
