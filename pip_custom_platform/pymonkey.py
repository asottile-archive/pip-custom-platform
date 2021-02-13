def pymonkey_argparse(argv):
    # We want to parse --platform out as early as possible so we can do patches
    # based on it
    import argparse
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--platform')
    return parser.parse_known_args(argv)


def pymonkey_patch(module, args):
    """
    This is where the magic happens:
        1. Monkey-patch `pip`'s `main` function, so that we can inject our own
           custom parser. This allows us to provide additional functionality
           (like `show-platform-name`) on top of the standard `pip` interface.

        2. Monkey-patch `pip`'s default functionality to identify the platform
           that the user is running on, and substitute it with our own (better)
           platform parser.
    """
    if module.__name__ == 'distutils.util':
        from pip_custom_platform.default_platform import get_platform_func
        module.get_platform = get_platform_func(args, module.get_platform)
    elif module.__name__ in ('pip.pep425tags', 'pip._internal.pep425tags'):
        from pip_custom_platform.default_platform import get_platform_func
        module.get_platform = get_platform_func(args, module.get_platform)
        module.supported_tags = module.get_supported()
        module.supported_tags_noarch = module.get_supported(noarch=True)
    elif (
        module.__name__ in ('pip', 'pip._internal') and
        hasattr(module, 'main')
    ):
        from pip_custom_platform._main import get_main
        module.main = get_main(module.main)
