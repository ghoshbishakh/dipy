#!/usr/bin/env python

from subprocess import Popen, PIPE, CalledProcessError, check_call
from os import chdir as cd


def sh(cmd):
    """Execute command in a subshell, return status code."""
    return check_call(cmd, shell=True)


def sh2(cmd):
    """Execute command in a subshell, return stdout.
    Stderr is unbuffered from the subshell.x"""
    p = Popen(cmd, stdout=PIPE, shell=True)
    out = p.communicate()[0]
    retcode = p.returncode
    if retcode:
        print(out.rstrip())
        raise CalledProcessError(retcode, cmd)
    else:
        return out.rstrip()


def sh3(cmd):
    """Execute command in a subshell, return stdout, stderr
    If anything appears in stderr, print it out to sys.stderr"""
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    out, err = p.communicate()
    retcode = p.returncode
    if retcode:
        raise CalledProcessError(retcode, cmd)
    else:
        return out.rstrip(), err.rstrip()


def buildDocs(tag):
    tag = tag.decode()

    # git checkout the specific tag:
    checkoutCall = "git checkout " + tag
    print(checkoutCall)
    checkout = sh2(checkoutCall)
    print(checkout)

    # build the checked out version:
    print(sh2("pwd"))
    cd("..")
    print(sh2("pwd"))
    sh2("sudo python setup.py build_ext -i")
    cd("doc")
    try:
        sh2("make api")
    except:
        print("API Build fail")
    sh2("make rstexamples")
    sh2("sphinx-build -b html -d _build/doctrees" + tag +
        "   . _build/html/" + tag)
    print("finished building docs for " + tag)
    checkout = sh3("git checkout sphinx_theme")


tags = sh2('git tag')
# exclude b'show', b'spag0.1' tags
tags = tags.split()[:-2]

# for now build only one version
# tags = tags[0]
print("Building docs for:", tags)

for tag in tags:
    print("Start building docs for ", tag)
    buildDocs(tag)

print("Checking out master head again")
