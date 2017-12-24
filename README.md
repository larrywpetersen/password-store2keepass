# **password-store2keepass**


password-store2keepass is a python script to convert a `password-store database`
into a `csv` file that can be imported into KeePass.

## Assumptions

It assumes that the password-store database has the password as the first line
(that should be pretty much standard).  It looks for lines that start with

`Username:`<br />
or<br />
`URL:`

These will be put into their fields in KeePass.

It also looks for a line that starts with

`Notes:`

everything after that will be put into the Notes field of KeePass.

These are *not* case sensitive.

Any other lines are unrecognized and will be put into a column labeled

`Other`

after the Notes column in the csv file.

As it reads the database, it will print messages for lines it does not
recognize and for files that it cannot read and decrypt.

The program asks for the *passphrase* so that it can decrypt the files.

It assumes that the GnuPG files are in `~/.gnupg`.

## Example

One argument is required and that is the password-store database directory.
For example,

`password-store2keepass keepass.csv`
<br />

## Dependencies

password-store2keepass requires `os`, `sys`, `csv`, and `gnupg`.

# Links

[Password-store site](https://www.passwordstore.org/)

[KeePass site](https://keepass.info/)
