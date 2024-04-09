#!/usr/bin/env python3

import argparse
from getpass import getpass
import requests
import os, sys, json
PROG = 'FavLinks'
AUTH_ENDPOINT = 'http://127.0.0.1:8000/api-token-auth/'

def show_info(args):
    if 'FAVLINKS' in os.environ:
        data = json.loads(os.environ['FAVLINKS'])
        print(data)
    else:
        print("Not logged-in. Please login with 'login' first.")

def register(args):
    """Register a new account."""
    print("New account")

def logout(args) -> bool:
    """Logout. If not logged-in, print that user is not logged-in and return."""
    if not 'FAVLINKS' in os.environ:
        print("User not logged-in.")
    else:
        print("Logging out....")

def login(args) -> bool:
    """Login to the service. Checks the 'FAVLINKS' in environment.
    Test:    
    curl -vv -X POST -H "Content-Type: application/json" -d '{"username":"value1", "password":"value2"}' http://127.0.0.1:8000/api-token-auth/
    """
    if 'FAVLINKS' in os.environ:
        print(os.environ['FAVLINKS'])
        return True
    username = args.username
    if not args.username:
        username = input("username: ")
    password = args.password
    if not args.password:
        password = getpass("password: ")
    data = json.dumps({'username': 'user', 'password': 'pass'})
    headers = {'Content-Type': 'application/json'}
    r = requests.post(AUTH_ENDPOINT,data=data,headers=headers)
    print(r)
    print(r.content)
    os.environ['FAVLINKS'] = json.dumps({'username': username})
    

def list_urls(args):
    """List my favorite URLs"""
    pass

def add_url(args):
    pass 

def remove_url(args):
    pass

def edit_url(args):
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

parser = argparse.ArgumentParser(prog=PROG,
                                 description=description,
                                 epilog=epilog)
parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="count")

group1 = parser.add_argument_group()
group1.add_argument('subcommand', help='choose sub-command', type=str, nargs='*', choices=action_table.keys())
group1.add_argument("-u", "--username", help="username for the account")
group1.add_argument("-p", "--password", help="username for the account")

parser.set_defaults(subcommand='info')

def main(args):
    if args.verbosity:
        print("verbosity turned on")
    if args.subcommand:
        print("Command: %s" % args.subcommand)
        cmd = args.subcommand[0]
        if cmd in action_table:
            action_table[cmd](args)
        else:
            parser.print_help()

if __name__ == '__main__':
    args = parser.parse_args()
    print("="*5 + PROG + "="*5)
    main(args)