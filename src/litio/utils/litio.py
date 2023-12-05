import rich, yaml, os

def run(args, get_module):
    if not os.path.exists('litio.yml'):
        rich.print(f"[bold red]Config file \"[bold yellow]litio.yml[/bold yellow]\" does not exist[/bold red]")
        exit(1)
    data = open('./litio.yml','r').read()
    data = yaml.safe_load(data)
    tests_output_args = get_module('utils').OutputArgs(title=data["name"])
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
                if function[function_name]["expected"].get('self'):
                    ... # Coming soon, acces to class self attributes
                if not function[function_name]["expected"].get('value'):
                    keys = list(function[function_name]["expected"].keys())
                    keys.pop(keys.index('comparator'))
                    value_name = keys[0]
                    assert_to = function[function_name]["expected"][value_name]
                    function[function_name]["expected"]["value"] = function[function_name]["expected"][value_name]
                    indexes = value_name.split('.')[1:]
                    argsDitctionary.update({
                        "assertion":function[function_name]["expected"]["comparator"],
                        "assert_to_dot": [assert_to,indexes]
                        })
                 
                else:
                    argsDitctionary.update({"assertion":function[function_name]["expected"]["comparator"], "assert_to":function[function_name]["expected"]["value"]})
            if function[function_name].get('instance'):
                argsDitctionary.update({"instance_params":function[function_name]["instance"]})
            argsDitctionary.update({"print_return":function[function_name].get('print-return') or args.verbose or function[function_name].get('verbose')})
            
            test_dict.update(argsDitctionary)
            new_params = {}
            for key, value in test_dict['params'].items():
                if type(value) == dict:
                    new_params[key] = value.copy()
                else:
                    new_params[key] = value
            test_dict['params'] = new_params
            argsToMain = get_module('utils').Args(argsDitctionary)

            main_response = get_module('tester').test(argsToMain, get_module)
            if not main_response:
                test_dict["status"] = {"passed": False, 'reason': "Function not found"}
                tests_output_args.add_test(test_dict, test)
                continue
            if isinstance(main_response, str) and args.ai:
                fixed_bug = get_module('ai').fix_bug(function_name=function_name, path=path, data=data, inputs=inputs, main_response=main_response, function=function, args=args)
                if not fixed_bug:
                    test_dict["status"] = {"passed": False, 'reason': "Could not fix bug"}
                    tests_output_args.add_test(test_dict, test)
                    continue
                if isinstance(fixed_bug, str):
                    test_dict['status'] = {"passed": False, 'reason': fixed_bug}
                    tests_output_args.add_test(test_dict, test)
                    continue
                to_print = main_response[0] if not test_dict.get('assert_to_dot') else main_response[2]
                assertion = fixed_bug[1]
            elif not main_response[1] and args.ai:
                fixed_bug = get_module('ai').fix_bug(function_name=function_name, path=path, data=data, inputs=inputs, main_response=main_response, function=function, args=args)
                if not fixed_bug:
                    test_dict["status"] = {"passed": False, 'reason': "Could not fix bug"}
                    tests_output_args.add_test(test_dict, test)
                    continue
                if isinstance(fixed_bug, str):
                    test_dict['status'] = {"passed": False, 'reason': fixed_bug}
                    tests_output_args.add_test(test_dict, test)
                    continue
                to_print = main_response[0] if not test_dict.get('assert_to_dot') else main_response[2]
                assertion = fixed_bug[1]
            else:
                to_print = main_response[0] if not test_dict.get('assert_to_dot') else main_response[2]
                assertion = main_response[1]
            
            if not assertion:
                comparator = function[function_name]['expected']['comparator']
                test_dict['status'] = {"passed": False, 'reason': f"{to_print} not {comparator} {function[function_name]['expected']['value']}"}
                tests_output_args.add_test(test_dict, test)
                continue
            test_dict['status'] = {"passed": assertion, 'reason': to_print}
            tests_output_args.add_test(test_dict, test)
    
    styles = get_module('output', True).copy()
    styles.pop('output')
    get_module('output').output(tests_output_args, args.output if args.output else data.get("output-style", "capybara"), styles)
