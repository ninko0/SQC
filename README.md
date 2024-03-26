# SQC
SQC for ssh quick config is a project who aims to be able to configure multiple machines or servers only in SSH and in a simple and quick way.
For the moment it only work on Debian based OS .

For the moment it is a little bit spagethi code, but I think all function to be replicable to add new options and new configuration very easly.

# Every thing is still in construction, you can read but it's not realy simple to understand

How to use :

pip install -r Requirement.txt # I did need to use "--break-system-packages" option probably because I am on a weird debian

python3 SQC.py -v

python3 SQC.py -h

some exemple of more complexe utilisation


Available function for now :

- apt update & upgrade the systeme
- add user 
- install list of any apt package
- gitclone list of tools
- change the SSH conf of your systeme
- change neplan (not opti, can cause colision of ip)

# TODO

install and conf apache with the possibility to hade x509 certs

create X509 autosigned certs

user and groupe with 1 cmd

install zsh with ohmyzsh and a theme of ohmyzsh given and sitch bash to zsh


