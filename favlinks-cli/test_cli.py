import pytest
from favlinks import main, parser

def test_parse_args():
    args = parser.parse_args([])
    with pytest.raises(SystemExit):
        main(args)
    assert True, "Argument for CLI parsed"

def test_parse_login():
    args = parser.parse_args(['login', '-u', 'test', '-p', 'test'])
    assert args.subcommand == ['login'], "CLI log-in command parsed: subcommand=%s" % args.subcommand


