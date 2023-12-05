import re


def extract_function_code(function_name, source_file):
    # Build the regex pattern to find the function
    if '.' in function_name:
        function_name = function_name.split('.')[1]
    function_pattern = re.compile(fr'(\bdef {function_name}\(.*?\):)(?:\n(.*?)(?=\n\s*def|\n\s*class|\n*$))?', re.DOTALL)
    
    with open(source_file, 'r') as file:
        content = file.read()

    # Search for the function in the file content
    matches = function_pattern.search(content)
    if matches:
        # The function was found, return the code
        function_declaration = matches.group(1)
        function_code = matches.group(2)
        function_code = "\n".join([function_declaration, function_code])
        
        lines = function_code.split('\n')
        line2 = lines[1]
        indentation = re.split(r'\w+', line2)[0]
        indentation = indentation.count(' ') + indentation.count('\t')
        
        function_code = f"{lines[0]}\n{lines[1]}"
        for line in lines[2:]:
            current_indentation = re.split(r'\w+', line)[0]
            current_indentation = current_indentation.count(' ') + current_indentation.count('\t')
            if current_indentation < indentation:
                break
            else:
                function_code += f"\n{line}"
        return function_code
    else:
        # The function was not found
        return None


class Args:
    def __init__(self, args):
        for key, value in args.items():
            setattr(self, key, value)

class Kwargs:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

def params_to_dict(params: list) -> dict:
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

class OutputArgs:
    def __init__(self, title: str, groups: list = []):
        self.title = title
        self.groups = groups
    def add_group(self, groups: dict):
        self.groups.append(groups)
    def add_test(self, test: dict, group_name: str):
        for group in self.groups:
            if group["name"] == group_name:
                group["tests"].append(test)