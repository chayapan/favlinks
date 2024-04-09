import argparse
import os, sys

def show_info():
    if not 'FAVLINKS' in os.environ:
        print("Not logged-in. Please login with 'login' first.")

def register():
    """Register a new account."""
    print("New account")

def logout():
    """Logout. If not logged-in, print that user is not logged-in and return."""
    if not 'FAVLINKS' in os.environ:
        print("User not logged-in.")
    else:
        print("logging out....")

def login():
    """Login to the service. Checks the 'FAVLINKS' in environment."""
    pass

def list_urls():
    """List my favorite URLs"""
    pass

def add_url():
    pass 

def remove_url():
    pass

def edit_url():
    pass

action_table = {
    'info': show_info,
    'register': register,
    'login': login,
    'logout': logout,
    'list': list_urls,
    'add': add_url,
    'remove': remove_url,
    'edit': edit_url
}

description='Manage your favorite URLs'
epilog='== Have a Nice Day ! =='

parser = argparse.ArgumentParser(prog='FavLinks',
                                 description=description,
                                 epilog=epilog)
parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="count")

group1 = parser.add_argument_group()
group1.add_argument('subcommand', help='choose sub-command', type=str, nargs='*', choices=action_table.keys())

parser.set_defaults(subcommand='info')

def main():
    args = parser.parse_args()
    if args.verbosity:
        print("verbosity turned on")
    if args.subcommand:
        print("Command: " + args.subcommand)
        cmd = args.subcommand
        if cmd in action_table:
            action_table[cmd]()

if __name__ == '__main__':
    main()