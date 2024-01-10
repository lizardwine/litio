import os, argparse, importlib, subprocess
from git import Repo

from . import litio, info, output, utils, tester, ai


def purge_dir(dir):
    if not os.path.exists(dir):
        return
    for f in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, f)):
            purge_dir(os.path.join(dir, f))
            os.rmdir(os.path.join(dir, f))
        else:
            os.remove(os.path.join(dir, f))

def install_module(args, get_module):
    module = args.module
    version = None
    if '@' in module:
        module, version = module.split('@')
    if not os.path.exists(f'./litio'):
        os.mkdir(f'./litio')
    if not os.path.exists(f'./litio/modules'):
        os.mkdir(f'./litio/modules')
    if args.upgrade and os.path.exists(f'./litio/modules/{module}'):
        purge_dir(f'./litio/modules/{module}')
        os.rmdir(f'./litio/modules/{module}')
    if os.path.exists(f'./litio/modules/{module}'):
        print(f"Module {module} already installed")
        return
    if not os.path.exists(f'./litio/modules/{module.split("/")[0]}'):
        os.mkdir(f'./litio/modules/{module.split("/")[0]}')
    os.mkdir(f'./litio/modules/{module}')
    
    
    repository = f'https://github.com/{module}.git'
    print(f"Installing module {module}...")
    repo = Repo.clone_from(repository, f'./litio/modules/{module}')
    if args.branch:
        try:
            repo.git.checkout(args.branch)
        except:
            print(f"Branch '{args.branch}' not found")
            print(f'Installing module at default branch...')
    if version:
        try:
            repo.git.checkout(version)
        except:
            print(f"Version '{version}' not found")
            print(f'Installing module at last version...')
    if 'requirements.txt' in os.listdir(f'./litio/modules/{module}'):
        print(f"Installing requirements for module {module}...")
        subprocess.run(['pip', 'install', '-r', f'./litio/modules/{module}/requirements.txt'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Module {module} installed successfully")

def remove_module(args, get_module):
    if not os.path.exists(f'./litio/modules/{args.module}'):
        print(f"Module {args.module} not installed")
        return
    
    purge_dir(f'./litio/modules/{args.module}')
    os.rmdir(f'./litio/modules/{args.module}')
    print(f"Module {args.module} removed successfully")

options = {
    'version': {
        'option': '--version',
        'aliases': ['-v'],
        'action': 'version',
        'version':'%(prog)s {}'.format(info.__version__)
    }
}

sub_commands = {
    'run': {
        'command': 'run',
        'help': 'run a litio test',
        'controller': litio.run,
        'options': {
            'verbose': {
                'option': '--verbose',
                'aliases': ['-V'],
                'dest': 'verbose',
                'help': 'enable verbosity',
                'required': False,
                'action': argparse.BooleanOptionalAction
            },
            'ai': {
                'option': '--ai',
                'dest': 'ai',
                'help': 'enable/disable ai',
                'required': False,
                'action': argparse.BooleanOptionalAction,
                'default': True,
            },
            'output': {
                'option': '--output',
                'aliases': ['-o'],
                'dest': 'output',
                'help': 'output style',
                'required': False,
                'default': None
            }
        }
    },
    'install': {
        'command': 'install',
        'help': 'install a litio module',
        'options': {
            'module': {
                'option': 'module',
                'help': 'module to install'
            },
            'upgrade': {
                'option': '--upgrade',
                'aliases': ['-u'],
                'help': 'upgrade a litio module',
                'required': False,
                'action': 'store_true'
            },
            'branch': {
                'option': '--branch',
                'aliases': ['-b'],
                'dest': 'branch',
                'default': None,
                'help': 'branch to get the module from',
                'required': False                
            }
        },
        'controller': install_module
    },
    'uninstall': {
        'command': 'uninstall',
        'help': 'uninstall a litio module',
        'options': {
            'module': {
                'option': 'module',
                'help': 'module to uninstall'
            }
        },
        'controller': remove_module
    }

}

modules_info = {
    'output': {
        'classic': output.output_classic,
        'capybara': output.capybara_output,
        'output': output.output
    },
    'options': options,
    'sub_commands': sub_commands,
    'utils': {
        'extract_function_code': utils.extract_function_code,
        'Args': utils.Args,
        'OutputArgs': utils.OutputArgs,
        'params_to_dict': utils.params_to_dict,
        'eval_params_values': utils.eval_params_values,
        'Kwargs': utils.Kwargs  
    },
    'tester': {
        'test': tester.test
    },
    'ai': {
        'BugFixer': ai.BugFixer,
        'fix_bug': ai.fix_bug
        
    }
}
def load_modules(safe_mode):
    if not os.path.exists('./litio/modules') or safe_mode:
        return modules_info
    for author in os.listdir(f'./litio/modules'):
        for module in os.listdir(f'./litio/modules/{author}'):
            if not os.path.exists(f'./litio/modules/{author}/{module}/litio.py'):
                continue
            spec = importlib.util.spec_from_file_location(f'{author}-{module}', f'./litio/modules/{author}/{module}/litio.py')
            modulelib = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulelib)
            for key, value in modulelib.litio.items():
                modules_info[key].update(value)
    return modules_info