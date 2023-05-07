import webbrowser
from onetwotext.cli import cli_arguments_machinery
from onetwotext.app import start_server, start_app


def main():
    """The main exposed via setuptools"""

    args = cli_arguments_machinery()
    if args.server:
        start_server(args.host, args.port)
    else:
        webbrowser.open_new_tab("http://localhost:8000/onetwotext")
        start_app()


if __name__ == "__main__":
    main()
