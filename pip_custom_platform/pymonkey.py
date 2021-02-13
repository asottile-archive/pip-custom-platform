# NOTE: These should be changed, depending on changes to pip's code layout
# over time. This requires a `main` function.
MAIN_MODULES = frozenset((
    'pip',                      # pip < 10
    'pip._internal',            # pip < 19.3
    'pip._internal.main',       # pip < 20
    'pip._internal.cli.main',   # pip ~ 20
))

# NOTE: This is a mapping between module_name, and function to monkey-patch.
PEP425_MODULES = {
    'pip.pep425tags': 'get_platform',               # pip < 9
    'pip._internal.pep425tags': 'get_platform',     # pip < 20
    'pip._vendor.packaging.tags': '_platform_tags'  # pip >= 20
}


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
    elif module.__name__ in PEP425_MODULES:
        _patch_pip_get_platform(module, args)
    elif module.__name__ in MAIN_MODULES and hasattr(module, 'main'):
        from pip_custom_platform._main import get_main
        module.main = get_main(module.main)


def _patch_pip_get_platform(module, args):
    """
    :type module: ModuleType
    :type args: argparse.Namespace
    """
    function_name = PEP425_MODULES[module.__name__]
    try:
        underlying_function = getattr(module, function_name)
    except AttributeError:
        return

    if isinstance(underlying_function(), str):
        from pip_custom_platform.default_platform import get_platform_func
        shimmed_function = get_platform_func
    else:
        from pip_custom_platform.default_platform import \
            get_multiple_platforms_func
        shimmed_function = get_multiple_platforms_func

    setattr(
        module,
        function_name,
        shimmed_function(args, underlying_function),
    )

    if hasattr(module, 'supported_tags'):
        module.supported_tags = module.get_supported()
        module.supported_tags_noarch = module.get_supported(noarch=True)
