import argparse
import importlib.util


parser = argparse.ArgumentParser(description='A command line function tester',epilog="Usage example: litio adding.py --function add --function-type function --params number1 200 number2 300")
parser.add_argument('file', metavar='file', type=str, help='file to execute')
parser.add_argument('--function',"-f",default="", help='function to execute',required=True)
parser.add_argument("--function-type","-t",dest="function_type",choices=("function","method","classmethod"),help='function type',required=True)
parser.add_argument('--instance-params',"-i",dest="instance_params", default="",nargs="*", help='params to pass to the function',required=False)
parser.add_argument('--params',"-p", default="",nargs="*", help='params to pass to the function',required=False)
parser.add_argument('--print-return', default=False, help='print return value',required=False,type=bool, action=argparse.BooleanOptionalAction)
parser.add_argument('--version','-v',action='version',version='%(prog)s 0.4.0.0')

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

def litio():
    module_name = 'module'
    spec = importlib.util.spec_from_file_location(module_name, args.file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # print(*list(module.__dict__.keys()),sep="\n")
    # print(list(getattr(module,"hello").__dict__.keys()))
    if args.function_type == "classmethod":
        _class = getattr(module,args.function.split(".")[0])
        function_params = _class.__dict__[args.function.split(".")[1]].__annotations__
    elif args.function_type == "method":
        _class = getattr(module,args.function.split(".")[0])
        function_params = _class.__dict__[args.function.split(".")[1]].__annotations__
    else:
        function_params = getattr(module,args.function).__annotations__
    params = params_to_dic(args.params)
    params = eval_params_values(params,function_params)
    if args.function_type == "method":
        init_params = getattr(module,args.function.split('.')[0]).__init__.__annotations__
        instance_params = params_to_dic(args.instance_params)
        instance_params = eval_params_values(instance_params,init_params)
    try:
        if args.function_type == "function":
            fun = getattr(module,args.function)
            if args.print_return:
                print(fun(**params))
            else:
                fun(**params)
        elif args.function_type == "method":
            class_name = args.function.split(".")[0]
            method_name = ".".join(args.function.split(".")[1:])
            _class = getattr(module,class_name)
            instance = _class(**instance_params)
            if args.print_return:
                print(getattr(instance,method_name)(**params))
            else:
                getattr(instance,method_name)(**params)
        elif args.function_type == "classmethod":
            if args.print_return:
                _class = getattr(module,args.function.split(".")[0])
                fun = getattr(_class,args.function.split(".")[1])
                print(fun(**params))
            else:
                _class = getattr(module,args.function.split(".")[0])
                fun = getattr(_class,args.function.split(".")[1])
                fun(**params)
    except Exception as e:
        print(str(e))