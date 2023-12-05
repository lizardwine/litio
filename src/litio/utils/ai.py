from openai import OpenAI
from dotenv import load_dotenv
import os
import rich


class BugFixer:
    def __init__(self, function, function_name, inputs, expected, returns, api_key):
        inputs = ", ".join([f"{key}={value}" for key, value in inputs.items()])
        self.prompt = f"function:\n{function}\nthe function name is: {function_name}\nthe expected value is {expected} when the input is: {inputs}\nthe function actually returns{' the error' if returns[1] else ''}: {returns[0]}"
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv(api_key))
        self.instructions = "fix the following code and response just and exclusively with the fixed code using the provided data, no explanations, retrieve the whole function"
    def get_fixed_function(self):        
        completion = self.client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": self.prompt},
        ]
        )
        return "\n".join(completion.choices[0].message.content.replace('\\n', '\n').replace('```','').splitlines()[1:])




def fix_bug(function_name, path, data, inputs, function, main_response, args, get_module):
    if function[function_name].get('use-ai') or function[function_name].get('auto-fix'):
        if function[function_name]["expected"].get("comparator") != "Equals":
            rich.print(f"[bold red]Test for {function_name}: Cannot use ai with assertion other than Equals[/bold red]")
            return
        if not data.get("api-key"):
            rich.print("[bold red]Cannot use ai without OpenAI api-key[/bold red]")
            return
        
        func_code = get_module('utils').extract_function_code(function_name, path)
        if not func_code:
            rich.print(f"[bold red]Test for {function_name}: Cannot find function code[/bold red]")
            return
        bug_fixer = get_module('ai').BugFixer(func_code, function_name, inputs, function[function_name]["expected"]["value"], [main_response if isinstance(main_response, str) else main_response[0], isinstance(main_response, str)], data["api-key"])
        if isinstance(main_response, str):
            bug = main_response
        else:
            bug = f"{main_response[0]} is not {function[function_name]['expected']['value']}"
        
        if function[function_name].get('auto-fix'):
            rich.print(f"[bold yellow]Auto fixing bug: '{bug}' in '{function_name}' using AI[/bold yellow]")
        else:
            fix_bug = input(f"Do you want to fix the bug: '{bug}' in '{function_name}' using AI? (Y/n) ")
            if fix_bug.lower() != "y":
                return
        fixed_bug = bug_fixer.get_fixed_function()
        with open(f"fixed_bug_{function_name}.tests.py", "w") as f:
            f.write(fixed_bug)
        
        print_return = function[function_name].get("print-return") or args.verbose or function[function_name].get("verbose")
        
        
        
        args_ditctionary = {
            "file": f"fixed_bug_{function_name}.tests.py",
            "function": function_name,
            "params": inputs,
            "assertion": function[function_name]["expected"]["comparator"],
            "assert_to": function[function_name]["expected"]["value"],
            "print_return": print_return
            
        }
        if function[function_name].get('instance'):
            args_ditctionary.update({"instance_params":function[function_name]["instance"]})
        
        args_for_main = get_module('utils').Args(args_ditctionary)
        
        test_fixed_bug = get_module('tester').test(args_for_main)
        if isinstance(test_fixed_bug, str):
            rich.print("[bold red]Bug fixed failed[/bold red]")
        rich.print("[bold green]Bug fixed successfully[/bold green]")
        if function[function_name].get('auto-fix'):
            rich.print("[bold yellow]Auto replacing the original code with the fixed code[/bold yellow]")
        else:
            replace = input("Do you want to replace the original code with the fixed code? (Y/n) ")
            if replace.lower() != "y":
                return
        all_code = open(path,'r').read()
        all_code = all_code.replace(func_code, fixed_bug)
        with open(path, 'w') as f:
            f.write(all_code)
        rich.print("[bold green]Code replaced successfully[/bold green]")
        os.remove(f"fixed_bug_{function_name}.tests.py")
        return test_fixed_bug
    return main_response