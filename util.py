import functools, inspect, sys

def constructor(__init__):
    @functools.wraps(__init__)
    def new_init(self, *args, **kwds):
        bound_args = inspect.signature(__init__).bind(self, *args, **kwds)
        if sys.version_info >= (3,5):
            bound_args.apply_defaults()
        for k, v in bound_args.arguments.items():
            setattr(self, k, v)
        __init__(self, *args, **kwds)
    return new_init

def accumulate(accum_type):
    def outer_wrapper(f):
        @functools.wraps(f)
        def inner_wrapper(*args, **kwds):
            return accum_type(iter(f(*args, **kwds)))
        return inner_wrapper
    return outer_wrapper

def accumulate_star(accum_type):
    return accumulate(lambda x: accum_type(*x))

def trace(show_counter=False, show_types=False):
    def outer_wrapper(f):
        counter = 0
        @functools.wraps(f)
        def inner_wrapper(*args):
            nonlocal counter
            counter += 1
            local_counter = counter

            if show_types:
                args_string = ', '.join(
                    '{}: {}'.format(arg, type(arg).__name__
                ) for arg in args)
            else:
                args_string = ', '.join(map(str, args))

            ret = f(*args)

            if show_counter:
                print(local_counter, end=' ')
            print('{}({}) -> {}'.format(f.__name__, args_string, ret))

            return ret
        return inner_wrapper
    return outer_wrapper
