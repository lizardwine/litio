import argparse
import os
import rich
import yaml
try:     
    from utils import ai, utils, tester, output, info
except ModuleNotFoundError:
    from .utils import ai, utils, tester, output, info


def litio():
    parser = argparse.ArgumentParser(description='A command line function tester')
    parser.add_argument('--version','-v',action='version',version='%(prog)s {}'.format(info.__version__))
    parser.add_argument('--config-file','-c',dest="config_file",help='config file',required=False, default="litio.yml")
    parser.add_argument('--verbose', '-V', dest="verbose", help="enable verbosity", required=False, action=argparse.BooleanOptionalAction)
    parser.add_argument('--ai', dest="ai", default=True ,help="enable/disable ai", required=False, action=argparse.BooleanOptionalAction)
    parser.add_argument('--output', dest="output", default=None, type=str, help="output style", required=False)
    
    args = parser.parse_args()

    if not os.path.exists(args.config_file):
        rich.print(f"[bold red]Config file \"[bold yellow]{args.config_file}[/bold yellow]\" does not exist[/bold red]")
        exit(1)
    data = open(args.config_file,'r').read()
    data = yaml.safe_load(data)
    tests_output_args = utils.OutputArgs(title=data["name"])
    for test, test_data in data["tests"].items():
        path = test_data['path']
        tests_output_args.add_group({
            "name": test,
            "path": path,
            "tests": []
        })
        for function in test_data['functions']:
            function_name = list(function.keys())[0]
            test_dict = {
                'name': function_name,
                'verbose': args.verbose or function[function_name].get('verbose')
            }
            if function[function_name].get('ignore'):
                test_dict['ignore'] = True
                tests_output_args.add_test(test_dict, test)
                continue
            
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
            
            test_dict.update(argsDitctionary)
            
            argsToMain = utils.Args(argsDitctionary)
            
            main_response = tester.test(argsToMain)
            if not main_response:
                test_dict["status"] = {"passed": False, 'reason': "Function not found"}
                tests_output_args.add_test(test_dict, test)
                continue
            if isinstance(main_response, str) and args.ai:
                fixed_bug = ai.fix_bug(function_name=function_name, path=path, data=data, inputs=inputs, main_response=main_response, function=function, args=args)
                if not fixed_bug:
                    test_dict["status"] = {"passed": False, 'reason': "Could not fix bug"}
                    tests_output_args.add_test(test_dict, test)
                    continue
                if isinstance(fixed_bug, str):
                    test_dict['status'] = {"passed": False, 'reason': fixed_bug}
                    tests_output_args.add_test(test_dict, test)
                    continue
                to_print = fixed_bug[0]
                assertion = fixed_bug[1]
            elif not main_response[1] and args.ai:
                fixed_bug = ai.fix_bug(function_name=function_name, path=path, data=data, inputs=inputs, main_response=main_response, function=function, args=args)
                if not fixed_bug:
                    test_dict["status"] = {"passed": False, 'reason': "Could not fix bug"}
                    tests_output_args.add_test(test_dict, test)
                    continue
                if isinstance(fixed_bug, str):
                    test_dict['status'] = {"passed": False, 'reason': fixed_bug}
                    tests_output_args.add_test(test_dict, test)
                    continue
                to_print = fixed_bug[0]
                assertion = fixed_bug[1]
            else:
                to_print = main_response[0]
                assertion = main_response[1]
            
            if not assertion:
                comparator = function[function_name]['expected']['comparator']
                test_dict['status'] = {"passed": False, 'reason': f"{to_print} not {comparator} {function[function_name]['expected']['value']}"}
                tests_output_args.add_test(test_dict, test)
                continue
            test_dict['status'] = {"passed": assertion, 'reason': to_print}
            tests_output_args.add_test(test_dict, test)
    output.output(tests_output_args, args.output if args.output else data.get("output-style", "capybara"))
    exit(0)

if __name__ == '__main__':
    litio()
