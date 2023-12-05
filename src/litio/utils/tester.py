import importlib.util

def test(args, get_module):
        module_name = 'module'
        spec = importlib.util.spec_from_file_location(module_name, args.file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if "." in args.function:
            module.__dict__
            _class = module.__dict__.get(args.function.split(".")[0], None)
            if not _class:
                return None
            function = _class.__dict__.get(args.function.split(".")[1])
            if not function:
                return None
            if type(function) == classmethod:
                function_type = "classmethod"
            else:
                function_type = "method"
            function_params = function.__annotations__
        else:
            function_type = "function"
            function_params = module.__dict__.get(args.function, None)
            if not function_params:
                return None
            function_params = function_params.__annotations__
        if type(args.params) == list:    
            params = get_module('utils').params_to_dict(args.params)
            params = get_module('utils').eval_params_values(params,function_params)
        else:
            params = args.params
        to_return_assert = None
        use_dot_to_return = False
        if function_type == "method":
            init_params = module.__dict__.get(args.function.split('.')[0]).__init__.__annotations__
            if type(args.instance_params) == list:    
                instance_params = get_module('utils').params_to_dict(args.instance_params)
                instance_params = get_module('utils').eval_params_values(instance_params,init_params)
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
            
            if args.__dict__.get('assert_to'):
                assert_to = args.__dict__.get('assert_to')
            else:
                assert_to, indexes = args.assert_to_dot
                use_dot_to_return = True
                dot_to_return = to_return
                last_return = to_return
                for index in indexes:
                    if isinstance(last_return, (list, tuple, set)):
                        if index.count(';') == 1:
                            index_0 = int(index.split(';')[0]) if index.split(';')[0].replace('-','').isdigit() else None
                            index_1 = int(index.split(';')[1]) if index.split(';')[1].replace('-','').isdigit() else None
                            last_return = last_return[index_0:index_1]
                        elif index.count(';') == 2:
                            index_0 = int(index.split(';')[0]) if index.split(';')[0].replace('-','').isdigit() else None
                            index_1 = int(index.split(';')[1]) if index.split(';')[1].replace('-','').isdigit() else None
                            index_2 = int(index.split(';')[2]) if index.split(';')[2].replace('-','').isdigit() else None
                            last_return = last_return[index_0:index_1:index_2]
                        else:
                            last_return = last_return[int(index)]
                    elif type(last_return) == dict:
                        last_return = last_return[index]
                    else:
                        try:
                            last_return = last_return.__dict__[index]
                        except KeyError:
                            return [f'{last_return.__class__.__name__} has no attribute {index}']
                to_return = last_return
            if args.assertion != None:
                if assert_to == None:
                    to_return_assert = ('No assertion to perform')
                if args.assertion == "Equals":
                    to_return_assert = (to_return == assert_to)
                elif args.assertion == "NotEquals":
                    to_return_assert = (to_return != assert_to)
                elif args.assertion == "Greater":
                    to_return_assert = (to_return > float(assert_to))
                elif args.assertion == "GreaterOrEquals":
                    to_return_assert = (to_return >= float(assert_to))
                elif args.assertion == "Less":
                    to_return_assert = (to_return < float(assert_to))
                elif args.assertion == "LessOrEquals":
                    to_return_assert = (to_return <= float(assert_to))
                elif args.assertion == "In":
                    to_return_assert = (to_return in eval(assert_to))
                elif args.assertion == "NotIn":
                    to_return_assert = (to_return not in eval(assert_to))
                elif args.assertion == "Is":
                    to_return_assert = (to_return is eval(assert_to))
                elif args.assertion == "IsNot":
                    to_return_assert = (to_return is not eval(assert_to))
                elif args.assertion == "IsNone":
                    to_return_assert = (to_return is None)
                elif args.assertion == "IsNotNone":
                    to_return_assert = (to_return is not None)
                elif args.assertion == "IsInstance":
                    to_return_assert = (to_return.__class__ == getattr(module,assert_to))
                elif args.assertion == "IsNotInstance":
                    to_return_assert = (to_return.__class__ != getattr(module,assert_to))
                else:
                    to_return_assert = False
                    to_return = (f"Assertion '{args.assertion}' not found")
            return [dot_to_return, to_return_assert, to_return] if use_dot_to_return else [to_return,to_return_assert]
        except Exception as e:
            return [dot_to_return, False, to_return] if use_dot_to_return else [to_return, False]
            