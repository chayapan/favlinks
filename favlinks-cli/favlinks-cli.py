#!/usr/bin/env python3
import shelve
import argparse
from getpass import getpass
import requests
import os, sys, json
PROG = 'FavLinks'
AUTH_ENDPOINT = 'http://127.0.0.1:8000/api-token-auth/'
INFO_ENDPOINT = 'http://127.0.0.1:8000/api/v1/users/{username}/'

def show_info(args):
    """Example:
    curl -vv -X GET -H "Authorization: Token 03d1f9f2b57ac5eb85228448dc706e3ed11bcaf5" http://127.0.0.1:8000/api/v1/users/
    """
    with shelve.open('favlinks.session') as session:
        if 'token' in session:
            print("User: " + session['username'])
            print("Token: " + session['token'])
        else:
            print("Not logged-in. Please login with 'login' first.")
        headers = {"Authorization": f"Token {session['token']}"}
        url = INFO_ENDPOINT.format(username=session['username'])
        r = requests.get(url, headers=headers)
        print("API: " + url)
        print(r.content.decode('utf-8'))

def register(args):
    """Register a new account."""
    print("New account")

def logout(args) -> bool:
    """Logout. If not logged-in, print that user is not logged-in and return."""
    with shelve.open('favlinks.session') as session:
        if 'token' in session:
            print(f"Logging out... {session['username']}")
            print(f"{session['token']}")
            del(session['token'])
        else:
            print("Not logged-in.")
            return False

def login(args) -> bool:
    """Login to the service. Checks the 'FAVLINKS' in environment.
    Test:    
    curl -vv -X POST -H "Content-Type: application/json" -d '{"username":"value1", "password":"value2"}' http://127.0.0.1:8000/api-token-auth/
    Example:
    ./favlinks-cli.py login --username test1 --password makePass3
    """
    with shelve.open('favlinks.session') as session:
        if 'token' in session:
            print("Already logged-in. User: " + session['username'])
            return True
    username = args.username
    if not args.username:
        username = input("username: ")
    password = args.password
    if not args.password:
        password = getpass("password: ")
    data = json.dumps({'username': username, 'password': password})
    headers = {'Content-Type': 'application/json'}
    r = requests.post(AUTH_ENDPOINT,data=data,headers=headers)
    content = r.content
    print(content.decode('utf-8'))
    res = json.loads(content.decode('utf-8'))
    if r.status_code == 200:
        with shelve.open('favlinks.session') as session:
            session['username'] =  username
            session['token'] = res['token']
        print("OK.")
        return True
    print("Error.")
    return False

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