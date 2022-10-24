import argparse
import os

parser = argparse.ArgumentParser(description='A command line function tester',epilog="Usage example: litio adding.py --function add --params number1 200 int number2 300 int")
parser.add_argument('file', metavar='file', type=str, help='file to execute')
parser.add_argument('--function',"-f", help='function to execute',required=True)
parser.add_argument('--params',"-p", default="",nargs="*", help='params to pass to the function',required=False)
parser.add_argument('--print-return', default=False, help='print return value',required=False,type=bool, action=argparse.BooleanOptionalAction)

args = parser.parse_args()

def params_to_dic(params: list) -> dict:
    dict_params = {}
    for i in range(0,len(params),3):
        param = {params[i]:{"value":params[i+1],"type":params[i+2]}}
        dict_params.update(param)

    return dict_params
def eval_params_values(params: dict) -> dict:
    for key,value in params.items():
        if value["type"] == "int":
            params[key]["value"] = int(value["value"])
        elif value["type"] != "str":
            params[key]["value"] = eval(value["value"])
        else:
            params[key]["value"] = f'"{value["value"]}"'
    return params
def extract_args(params: dict) -> str:
    arguments = ""
    for key, value in params.items():
        arguments += key + "=" + str(value["value"]) + (", " if key != list(params.keys())[-1] else "")
    return arguments
def litio():
    exec("import importlib.util;" + \
    f"spec = importlib.util.spec_from_file_location('{args.file.replace('.py','')}','{os.path.join(os.getcwd(),args.file)}');" + \
    "lib = importlib.util.module_from_spec(spec);"
    "spec.loader.exec_module(lib);" + \
    f"fun = lib.{args.function}")
    params = params_to_dic(args.params)
    params = eval_params_values(params)
    arguments = extract_args(params)
    try:
        if args.print_return:
            exec(f"print(fun({arguments}))")
        else:
            exec(f"fun({arguments})")
    except Exception as e:
        print(str(e))