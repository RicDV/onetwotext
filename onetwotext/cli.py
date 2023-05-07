from typing import Optional, List
import argparse
import sys

from . import __version__


class CustomVersionAction(argparse.Action):
    """A custom argparse Action to show the program version and exit."""

    def __init__(self, option_strings, dest, nargs=0, **kwargs):
        super().__init__(option_strings, dest, nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        """print the program version
        along with the name and version of the plugin addresss package (if found)
        and quit the program returning 0 as return code
        """
        print(f"{__package__}, version {__version__}")
        sys.exit(0)


def cli_arguments_machinery(raw_args: Optional[List[str]] = None):
    """Setup of argparser and actually CLI arguments parsing"""

    parser = argparse.ArgumentParser(
        description="A command line interface for onetwotext",
    )
    parser.add_argument(
        "-v",
        "--version",
        action=CustomVersionAction,
        help="show program's version number and exit",
    )
    parser.add_argument(
        "-s",
        "--server",
        action="store_true",
        default=False,
        help="Expose Server-side app.",
    )
    parser.add_argument(
        "-hs", "--host", type=str, help="Host app is listening on.", default="0.0.0.0"
    )
    parser.add_argument(
        "-p", "--port", type=str, help="Port app is listening on.", default="8080"
    )

    args = parser.parse_args(raw_args)
    return args
