import pytest

url = "postgres://bob@psqlserver:5432/db_one"

def test_parser_without_driver():
    """
    Without a specified driver the parser will exit
    """
    with pytest.raises(SystemExit):
        parser = cli.create_parser()
        parser.parse_args([url])

def test_parser_with_driver():
    """
    The parser will fail without a destination
    """
    parser = cli.create_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([url, "--driver", "local"])

# happy path
def test_parser_with_driver_and_destination():
    """
    The parser will not exit if it receives a driver and destination
    """
    parser = cli.create_parser()

    args.parser.parse_args(["url", "--driver", "local", "/some/path"])
    assert args.driver == "local"
    assert args.destination == "/some/path"