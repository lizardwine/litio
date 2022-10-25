import argparse
import os

parser = argparse.ArgumentParser(description='A command line function tester',epilog="Usage example: litio adding.py --function add --function-type function --params number1 200 number2 300")
parser.add_argument('file', metavar='file', type=str, help='file to execute')
parser.add_argument('--function',"-f",default="", help='function to execute',required=True)
parser.add_argument("--function-type","-t",dest="function_type",choices=("function","method","classmethod"),help='function type',required=True)
parser.add_argument('--instance-params',"-i",dest="instance_params", default="",nargs="*", help='params to pass to the function',required=False)
parser.add_argument('--params',"-p", default="",nargs="*", help='params to pass to the function',required=False)
parser.add_argument('--print-return', default=False, help='print return value',required=False,type=bool, action=argparse.BooleanOptionalAction)

args = parser.parse_args()

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
            params[key] = f'"{value}"'
    return params
def extract_args(params: dict) -> str:
    arguments = ""
    for key, value in params.items():
        arguments += key + "=" + str(value) + (", " if key != list(params.keys())[-1] else "")
    return arguments
def litio():
    directory = os.path.join(os.getcwd(),args.file).replace("\\","/")
    exec("import importlib.util;" + \
    f"spec = importlib.util.spec_from_file_location('{args.file.replace('.py','')}','{directory}');" + \
    "lib = importlib.util.module_from_spec(spec);" + \
    "spec.loader.exec_module(lib);")
    exec(f"global functions;functions = lib.{args.function}.__annotations__")
    exec(f"global init_functions;init_functions = lib.{args.function.split('.')[0]}.__init__.__annotations__")
    params = params_to_dic(args.params)
    params = eval_params_values(params,functions)
    arguments = extract_args(params)
    instance_params = params_to_dic(args.instance_params)
    instance_params = eval_params_values(instance_params,init_functions)
    instance_args = extract_args(instance_params)
    try:
        if args.function_type == "function":
            exec(f"fun = lib.{args.function}")
            if args.print_return:
                exec(f"print(fun({arguments}))")
            else:
                exec(f"fun({arguments})")
        elif args.function_type == "method":
            class_name = args.function.split(".")[0]
            method_name = ".".join(args.function.split(".")[1:])
            exec(f"clas = lib.{class_name}")
            exec(f"ins = clas({instance_args})")
            if args.print_return:
                exec(f"print(ins.{method_name}({arguments}))")
            else:
                exec(f"ins.{method_name}({arguments})")
        elif args.function_type == "classmethod":
            if args.print_return:
                exec(f"print(lib.{args.function}({arguments}))")
            else:
                exec(f"lib.{args.function}({arguments})")
    except Exception as e:
        print(str(e))
