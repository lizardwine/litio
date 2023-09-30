
class Args:
    def __init__(self, args):
        for key, value in args.items():
            setattr(self, key, value)