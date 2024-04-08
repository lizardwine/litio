import os, argparse, importlib, subprocess
from git import Repo
import json
from . import litio, info, output, utils, tester, ai
import tarfile


def uncompress(source, dest):
    with tarfile.open(source, "r:gz") as tar:
        tar.extractall(path=dest)

def purge_dir(dir):
    if not os.path.exists(dir):
        return
    for f in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, f)):
            purge_dir(os.path.join(dir, f))
            os.rmdir(os.path.join(dir, f))
        else:
            os.remove(os.path.join(dir, f))

def prepare_for_install():
    if not os.path.exists(f'./litio'):
        os.mkdir(f'./litio')
    if not os.path.exists(f'./litio/modules'):
        os.mkdir(f'./litio/modules')
    if not os.path.exists(f'./litio/modules/.dev'):
        os.mkdir(f'./litio/modules/.dev')

def install_module(args, get_module):
    module = args.module
    version = None
    if module.endswith('.tar.gz'):
        prepare_for_install()
        name = ".".join(module.split(".")[:-2])
        name = name.split("/")[-1]
        no_version_name = "-".join(name.split("-")[:-1])
        print("Installing module from tarball")
        for f in os.listdir('./litio/modules/.dev'):
            if no_version_name in f:
                purge_dir(f'./litio/modules/.dev/{f}')
                os.rmdir(f'./litio/modules/.dev/{f}')
        uncompress(module, f'./litio/modules/.dev/{name}')
        if 'requirements.txt' in os.listdir(f'./litio/modules/.dev/{name}/'):
            print(f"Installing requirements for module {name}...")
            subprocess.run(['pip', 'install', '-r', f'./litio/modules/.dev/{name}/requirements.txt'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Module {name} installed successfully")
        return
        
    if '@' in module:
        module, version = module.split('@')
    prepare_for_install()
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

def pack_module(args, get_module):
    required_files = ["litio.py", "litio.json"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"Required file {file} not found")
            return
    ignore = ["dist"]
    if os.path.exists('./.litioignore'):
        ignore += open('./.litioignore', 'r').read().splitlines()
    package_data = json.load(open('./litio.json', 'r'))
    if not package_data.get('name'):
        print('Missing name in litio.json')
        return
    if not package_data.get('version'):
        print('Missing version in litio.json')
        return
    if not os.path.exists('./dist/'):
        os.mkdir('./dist/')
    else:
        purge_dir('./dist/')
    tar = tarfile.open(f'./dist/{package_data["name"]}-{package_data["version"]}.tar.gz', 'w:gz')
    for file in os.listdir('./'):
        if file in ignore and not file in required_files:
            continue
        tar.add(file)
    tar.close()
    print("Module packed successfully")

options = {
    'version': {
        'option': '--version',
        'aliases': ['-v'],
        'action': 'version',
        'version':'%(prog)s v{}'.format(info.__version__)
    }
}

sub_commands = {
    'pack': {
        'command': 'pack',
        'help': 'pack a litio module',
        'controller': pack_module,
        'options': {
            
        }
    },
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
    modules = os.listdir(f'./litio/modules')
    modules = [module for module in modules if module != ".dev"]
    for author in modules:
        for module in os.listdir(f'./litio/modules/{author}'):
            if not os.path.exists(f'./litio/modules/{author}/{module}/litio.py'):
                continue
            spec = importlib.util.spec_from_file_location(f'{author}-{module}', f'./litio/modules/{author}/{module}/litio.py')
            modulelib = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulelib)
            for key, value in modulelib.litio.items():
                modules_info[key].update(value)
    for module in os.listdir('./litio/modules/.dev'):
        if not os.path.exists(f'./litio/modules/.dev/{module}/litio.py'):
            continue
        spec = importlib.util.spec_from_file_location(f'.dev-{module}', f'./litio/modules/.dev/{module}/litio.py')
        modulelib = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulelib)
        for key, value in modulelib.litio.items():
            modules_info[key].update(value)
    return modules_info