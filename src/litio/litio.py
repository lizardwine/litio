import argparse
try:     
    from utils import modules
except ModuleNotFoundError:
    from .utils import modules


def litio():
    parser = argparse.ArgumentParser(description='A command line function tester')

    modules_info = modules.load_modules()
    def get_module(module_name, info=False):
        if info:
            return modules_info[module_name]
        return modules_info['utils']['Kwargs'](**modules_info[module_name])
    
    for option in list(modules_info['options'].values()): # Load options and add them to the parser
        name = option['option']
        aliases = option.get('aliases', [])
        flags_or_name = [name] + aliases
        if option.get('aliases'):
            option.pop('aliases')
        option.pop('option')
        parser.add_argument(*flags_or_name, **option)
    subparsers = parser.add_subparsers(help='sub-command help')
    for sub_command in list(modules_info['sub_commands'].values()):
        command = sub_command['command']
        sub_parser = subparsers.add_parser(name=command, help=sub_command.get('help'))
        for option in list(sub_command['options'].values()): # Load options and add them to the sub parser
            name = option['option']
            aliases = option.get('aliases', [])
            flags_or_name = [name] + aliases
            if option.get('aliases'):
                option.pop('aliases')
            option.pop('option')
            sub_parser.add_argument(*flags_or_name, **option)
        sub_parser.set_defaults(func=sub_command['controller'])
    
    args = parser.parse_args()
    args.func(args, get_module)
    exit(0)

if __name__ == '__main__':
    litio()
