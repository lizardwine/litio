import rich
from . import utils, info

def output_classic(args: utils.OutputArgs):
    rich.print(f"[bold cyan]{args.title}[/bold cyan]")
    for group in args.groups:
        rich.print(f"[bold blue]{' '*4}- {group['name']}[/bold blue]")
        for test in group["tests"]:
            rich.print(f"[bold magenta]{' '*8}- {test['name']}[/bold magenta]")
            if test.get('ignore'):
                rich.print(f"[bold red]{' '*12}-Test: ignored[/bold red]")
                continue
            if not test['verbose']:
                if test['status']['passed']:
                    rich.print(f"[bold green]{' '*12}-Test: passed[/bold green]")
                else:
                    returned = test['status']['reason']
                    returned = f"'{returned}'" if isinstance(returned, str) else returned
                    rich.print(f"[bold red]{' '*12}-Test: failed: {returned}[/bold red]")
                continue
            if test['params'] != {}:
                rich.print(f"[bold yellow]{' '*12}- inputs:[/bold yellow]")
                for key, value in test['params'].items():
                    value = f"'{value}'" if isinstance(value, str) else value
                    rich.print(f"[bold yellow]{' '*14}- {key}: {value}[/bold yellow]")
            if test.get('instance_params'):
                rich.print(f"[bold yellow]{' '*12}- instance:[/bold yellow]")
                for key, value in test['instance_params'].items():
                    value = f"'{value}'" if isinstance(value, str) else value
                    rich.print(f"[bold yellow]{' '*14}- {key}: {value}[/bold yellow]")
            assert_to = test['assert_to']
            assert_to = f"'{assert_to}'" if isinstance(assert_to, str) else assert_to
            returned = test['status']['reason']
            returned = f"'{returned}'" if isinstance(returned, str) else returned
            
            rich.print(f"[bold yellow]{' '*12}- assertion: {test['assertion']}[/bold yellow]")
            rich.print(f"[bold yellow]{' '*12}- assert to: {assert_to}[/bold yellow]")
            rich.print(f"[bold yellow]{' '*12}- returned: {returned}[/bold yellow]")
            if test['status']['passed']:
                rich.print(f"[bold green]{' '*12}-Test: passed[/bold green]")
            else:
                rich.print(f"[bold red]{' '*12}-Test: failed[/bold red]")

def capybara_output(args: utils.OutputArgs):
    rich.print(f"[bold blue]Litio[/bold blue][bold green]@[/bold green][bold blue]{info.__version__}[/bold blue] - [bold green]{args.title}[/bold green]")
    for group in args.groups:
        group_name = group["name"]
        group_name = group_name.replace("-", " ").replace("_", " ")
        group_name = group_name.title()
        passed_tests = len([test for test in group["tests"] if test.get('status', {'passed': False}).get('passed')])
        not_passed_tests = len([test for test in group["tests"] if not test.get('status', {'passed': True}).get('passed')])
        ignored = len([test for test in group["tests"] if test.get("ignore")])
        print(f"[{group_name}] ✔️  Passed {passed_tests} ❌ Errors {not_passed_tests}  ⚠️  Ignored {ignored}")
        most_largest_name = max(len(test["name"]) for test in [group for group in args.groups])
        
        for test in group["tests"]:
            if test.get('ignore'):
                tabs = most_largest_name + 6 - len(test['name'])
                tabs = ' '*tabs
                print(f"{' '*3}- {test['name']}{tabs}⚠️  Ignored")
                continue
            if test['status']['passed']:
                tabs = most_largest_name + 6 - len(test['name'])
                tabs = ' '*tabs

                print(f"{' '*3}- {test['name']}{tabs}{'✔️  Passed'}")
            else:
                tabs = most_largest_name + 6 - len(test['name'])
                tabs = ' '*tabs
                print(f"{' '*3}- {test['name']}{tabs}{'❌  Error'} \"{test['status']['reason']}\"")
        print() # new line
outputs = {
    'classic': output_classic,
    'capybara': capybara_output
}

def output(args: utils.OutputArgs, style):
    outputs.get(style, capybara_output)(args)