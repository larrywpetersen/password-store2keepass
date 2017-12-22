#!/usr/bin/python

import csv
import os
import sys
import gnupg
from scanner import StringScanner, StringRegexp


def traverse(path):
    for root, dirs, files in os.walk(path):
        if '.git' in dirs:
            dirs.remove('.git')
        for name in files:
            yield os.path.join(root, name)


def parse(basepath, path, data):
    name = os.path.splitext(os.path.basename(path))[0]
    group = os.path.dirname(os.path.os.path.relpath(path, basepath))
#    split_data = data.split('\n', maxsplit=1)
    split_data = data.split('\n' )
    password = split_data[0]
    if len( split_data) > 1:
        notes = split_data[1]
    else:
        notes = ''
    return [group, name, password, notes]


def main(path):

    gpg = gnupg.GPG( homedir='~/.gnupg' )
    gpg.encoding = 'utf-8'
    csv_data = []
    csv_data.append( [ 'Group', 'Title', 'Username', 'Password',
                            'URL', 'Notes', 'Unrecognized'] )

    print

    MyPassPhrase = raw_input( 'Passphrase: ')

    # print 'path = ' + path

    for file_path in traverse(path):
        if os.path.splitext(file_path)[1] == '.gpg':
            f = open( file_path, 'rb')
            data = gpg.decrypt_file(f, passphrase=MyPassPhrase)
            sys.stdout.write( '.')
            sys.stdout.flush()
            if data.ok:
                # i = file_path.rfind( '/')
                # file = file_path[ i+1: ]
                # print file_path
                d = data.data
                i = d.find( '\n')
                pw = d[ :i ]
                d = d[ i+1: ]
                uname = ''
                url = ''
                notes = ''
                other = ''
                while len( d) > 0:
                    i = d.find( '\n')
                    l = d[ :i ] + ' '
                    # print type( l)
                    # print l
                    if l.lower().startswith( 'username:'):
                        uname = l[ 9: ].strip()
                    elif l.lower().startswith( 'url:'):
                        url = l[ 4].strip()
                    elif l.lower().startswith( 'notes:'):
                        notes = d[ 6: ]
                        d = ''
                    elif l.lower().startswith( 'note:'):
                        notes = d[ 6: ]
                        d = ''
                    else:
                        other = other + '\n' + l
                        print '\n\nUnrecognized line in ' + file_path + '\n'

                    other = other
                    name = os.path.splitext(os.path.basename(file_path))[0]
                    group = os.path.dirname(os.path.os.path.relpath(file_path, path))
                    if len( group) > 0:
                        title = group + '/' + name
                    else:
                        title = name
                    # csv_line =[ file, uname, pw, url, notes, other]
                    csv_line = [ 'Root/' + group, name, uname, pw, url, notes, other]
                    if len( d) > 0:
                        d = d[ i+1: ]
                csv_data.append( csv_line)
                # print pw + ' - ' + uname
            else:
                print '\n\nProblem with ' + file_path + '\n'


    with open('pass.csv', 'w' ) as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(csv_data)

    print '\n'


if __name__ == '__main__':
    if len( sys.argv) > 1:
        path = os.path.abspath(sys.argv[1])
        main(path)
    else:
        print 'Usage: password-store2keepass.py PASSWORD-STORE-DIRECTORY'
