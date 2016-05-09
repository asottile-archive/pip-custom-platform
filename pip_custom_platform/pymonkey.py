def pymonkey_argparse(argv):
    def _add_platform_param(parser):
        parser.add_argument(
            '--platform', help=(
                'Custom platform name.  The default is auto-detected -- '
                'Use `pip-custom-platform show-platform-name` to show.'
            ),
        )

    import argparse
    parser = argparse.ArgumentParser(
        description=(
            'pip+wheel wrapper which allows you to choose a custom platform '
            'name for building, downloading, and installing wheels.\n\n'
            'Any unparsed command arguments will be passed on to pip\n'
        ),
    )
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    install = subparsers.add_parser('install', help='Install packages')
    _add_platform_param(install)

    download = subparsers.add_parser('download', help='Download packages')
    _add_platform_param(download)

    platform_name = subparsers.add_parser(
        'show-platform-name', help='Show the default platform name',
    )
    _add_platform_param(platform_name)

    wheel = subparsers.add_parser('wheel', help='Build wheels')
    _add_platform_param(wheel)
    wheel.add_argument(
        '-w', '--wheel-dir', help='Build wheels into this directory',
        default='./wheelhouse',
    )

    args, argv = parser.parse_known_args(argv)
    # Put the command back so pip will work
    argv = [args.command] + argv
    return args, argv


def pymonkey_patch(mod, args):
    if mod.__name__ == 'distutils.util':
        from pip_custom_platform.default_platform import get_platform_func
        mod.get_platform = get_platform_func(args, mod.get_platform)
    # Need some special logic in pip.main for wheel
    elif mod.__name__ == 'pip' and args.command == 'wheel':
        from pip_custom_platform.wheel import get_wheel_main
        mod.main = get_wheel_main(mod.main, args)
    elif mod.__name__ == 'pip' and args.command == 'show-platform-name':
        from pip_custom_platform.default_platform import get_platform_main
        mod.main = get_platform_main()
