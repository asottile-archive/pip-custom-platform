def pytest_addoption(parser):
    # The Docker tests are ridiculously slow (~1 hour), take a bunch of disk
    # space, and are flaky by nature. So let's not run them by default (we have
    # mocks as well as the Docker integration tests).
    parser.addoption(
        '--docker',
        action='store_true',
        default=False,
        help='Run Docker tests (very slow, takes lots of disk space)',
    )
