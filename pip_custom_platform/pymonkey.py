def pymonkey_argparse(argv):
    # We want to parse --platform out as early as possible so we can do patches
    # based on it
    import argparse
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--platform')
    return parser.parse_known_args(argv)


def pymonkey_patch(mod, args):
    if mod.__name__ == 'distutils.util':
        from pip_custom_platform.default_platform import get_platform_func
        mod.get_platform = get_platform_func(args, mod.get_platform)
    elif mod.__name__ in ('pip.pep425tags', 'pip._internal.pep425tags'):
        from pip_custom_platform.default_platform import get_platform_func
        mod.get_platform = get_platform_func(args, mod.get_platform)
        mod.supported_tags = mod.get_supported()
        mod.supported_tags_noarch = mod.get_supported(noarch=True)
    elif mod.__name__ in ('pip', 'pip._internal') and hasattr(mod, 'main'):
        from pip_custom_platform._main import get_main
        mod.main = get_main(mod.main)
