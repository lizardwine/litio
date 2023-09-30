import argparse
import importlib.util


parser = argparse.ArgumentParser(description='A command line function tester',epilog="Usage example: litio adding.py --function add --function-type function --params number1 200 number2 300")
parser.add_argument('file', metavar='file', type=str, help='file to execute')
parser.add_argument('--function',"-f",default="", help='function to execute',required=True)
parser.add_argument('--instance-params',"-i",dest="instance_params", default="",nargs="*", help='params to instance the class(used for tests methods)',required=False)
parser.add_argument('--params',"-p", default="",nargs="*", help='params to pass to the function',required=False)
parser.add_argument('--print-return', default=False, help='print return value',required=False,type=bool, action=argparse.BooleanOptionalAction)
parser.add_argument('--assert','-a', dest="assertion", choices=('Equals', 'NotEquals', 'Greater', 'GreaterOrEquals', 'Less', 'LessOrEquals', 'In', 'NotIn', 'Is', 'IsNot', 'IsNone', 'IsNotNone', 'IsInstance', 'IsNotInstance'),help='assert return value',required=False)
parser.add_argument('--assert-to',"-x", dest="assert_to",help='assert to',required=False)
parser.add_argument('--version','-v',action='version',version='%(prog)s 0.4.2.2')

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
            params[key] = f'{value}'
    return params

def litio():
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
        return_type = function.__annotations__.get("return")
    else:
        function_type = "function"
        function_params = getattr(module,args.function).__annotations__
        return_type = function_params.get("return")
        
    params = params_to_dic(args.params)
    params = eval_params_values(params,function_params)
    return_value = None
    if function_type == "method":
        init_params = getattr(module,args.function.split('.')[0]).__init__.__annotations__
        instance_params = params_to_dic(args.instance_params)
        instance_params = eval_params_values(instance_params,init_params)
    try:
        if function_type == "function":
            fun = getattr(module,args.function)
            if args.print_return:
                return_value = fun(**params)
                print(return_value)
            else:
                return_value = fun(**params)
        elif function_type == "method":
            class_name = args.function.split(".")[0]
            method_name = ".".join(args.function.split(".")[1:])
            _class = getattr(module,class_name)
            instance = _class(**instance_params)
            if args.print_return:
                return_value = getattr(instance,method_name)(**params)
                print(return_value)
            else:
                return_value = getattr(instance,method_name)(**params)
        elif function_type == "classmethod":
            if args.print_return:
                _class = getattr(module,args.function.split(".")[0])
                fun = getattr(_class,args.function.split(".")[1])
                return_value = fun(**params)
                print(return_value)
            else:
                _class = getattr(module,args.function.split(".")[0])
                fun = getattr(_class,args.function.split(".")[1])
                return_value = fun(**params)
    
        if args.assertion != None:
            if args.assert_to == None:
                print('No assertion to perform')
                exit(1)
            if args.assertion == "Equals":
                if return_type == str:
                    print(return_value == args.assert_to)
                elif return_type in [int,float]:
                    print(return_value == float(args.assert_to))
                else:
                    print(return_value == eval(args.assert_to))
            elif args.assertion == "NotEquals":
                print(return_value != eval(args.assert_to))
            elif args.assertion == "Greater":
                print(return_value > float(args.assert_to))
            elif args.assertion == "GreaterOrEquals":
                print(return_value >= float(args.assert_to))
            elif args.assertion == "Less":
                print(return_value < float(args.assert_to))
            elif args.assertion == "LessOrEquals":
                print(return_value <= float(args.assert_to))
            elif args.assertion == "In":
                print(return_value in eval(args.assert_to))
            elif args.assertion == "NotIn":
                print(return_value not in eval(args.assert_to))
            elif args.assertion == "Is":
                print(return_value is eval(args.assert_to))
            elif args.assertion == "IsNot":
                print(return_value is not eval(args.assert_to))
            elif args.assertion == "IsNone":
                print(return_value is None)
            elif args.assertion == "IsNotNone":
                print(return_value is not None)
            elif args.assertion == "IsInstance":
                print(return_value.__class__ == getattr(module,args.assert_to))
            elif args.assertion == "IsNotInstance":
                print(return_value.__class__ != getattr(module,args.assert_to))
    except Exception as e:
        print(str(e))
        exit(1)
litio()