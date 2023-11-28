import importlib.util
import rich
from . import utils

def test(args: utils.Args):
        module_name = 'module'
        spec = importlib.util.spec_from_file_location(module_name, args.file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if "." in args.function:
            _class = getattr(module,args.function.split(".")[0], None)
            if not _class:
                rich.print("[bold red]           - Class not found[/bold red]")
                return None
            function = _class.__dict__.get(args.function.split(".")[1])
            if not function:
                rich.print("[bold red]           - Method not found[/bold red]")
                return None
            if type(function) == classmethod:
                function_type = "classmethod"
            else:
                function_type = "method"
            function_params = function.__annotations__
        else:
            function_type = "function"
            function_params = getattr(module,args.function, None)
            if not function_params:
                rich.print("[bold red]           - Function not found[/bold red]")
                return None
            function_params = function_params.__annotations__
        if type(args.params) == list:    
            params = utils.params_to_dic(args.params)
            params = utils.eval_params_values(params,function_params)
        else:
            params = args.params
        to_return_assert = None
        if function_type == "method":
            init_params = getattr(module,args.function.split('.')[0]).__init__.__annotations__
            if type(args.instance_params) == list:    
                instance_params = utils.params_to_dic(args.instance_params)
                instance_params = utils.eval_params_values(instance_params,init_params)
            else:
                instance_params = args.instance_params
        try:
            if function_type == "function":
                fun = getattr(module,args.function)
                try:
                    to_return = fun(**params)
                except Exception as e:
                    return str(e)

            elif function_type == "method":
                class_name = args.function.split(".")[0]
                method_name = ".".join(args.function.split(".")[1:])
                _class = getattr(module,class_name)
                instance = _class(**instance_params)
                try:
                    to_return = getattr(instance,method_name)(**params)
                except Exception as e:
                    return str(e)

            elif function_type == "classmethod":
                _class = getattr(module,args.function.split(".")[0])
                fun = getattr(_class,args.function.split(".")[1])
                try:
                    to_return = fun(**params)
                except Exception as e:
                    return str(e)

            if args.assertion != None:
                if args.assert_to == None:
                    to_return_assert = ('No assertion to perform')
                if args.assertion == "Equals":
                    to_return_assert = (to_return == args.assert_to)
                elif args.assertion == "NotEquals":
                    to_return_assert = (to_return != args.assert_to)
                elif args.assertion == "Greater":
                    to_return_assert = (to_return > float(args.assert_to))
                elif args.assertion == "GreaterOrEquals":
                    to_return_assert = (to_return >= float(args.assert_to))
                elif args.assertion == "Less":
                    to_return_assert = (to_return < float(args.assert_to))
                elif args.assertion == "LessOrEquals":
                    to_return_assert = (to_return <= float(args.assert_to))
                elif args.assertion == "In":
                    to_return_assert = (to_return in eval(args.assert_to))
                elif args.assertion == "NotIn":
                    to_return_assert = (to_return not in eval(args.assert_to))
                elif args.assertion == "Is":
                    to_return_assert = (to_return is eval(args.assert_to))
                elif args.assertion == "IsNot":
                    to_return_assert = (to_return is not eval(args.assert_to))
                elif args.assertion == "IsNone":
                    to_return_assert = (to_return is None)
                elif args.assertion == "IsNotNone":
                    to_return_assert = (to_return is not None)
                elif args.assertion == "IsInstance":
                    to_return_assert = (to_return.__class__ == getattr(module,args.assert_to))
                elif args.assertion == "IsNotInstance":
                    to_return_assert = (to_return.__class__ != getattr(module,args.assert_to))
            return [to_return,to_return_assert]
        except Exception as e:
            return to_return, False