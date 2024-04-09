from favlinks import main, parser

def test_parse_login():
    parser.parse_args(['a', '--help'])
    assert False, "Argument for CLI parsed"


def test_parse_args():
    main()
    assert False, "Argument for CLI parsed"