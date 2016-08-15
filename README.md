# python-langsax
This is a tool to tunnel TCP connections through an HTTP Proxy. It was inspired by corkscrew.

But since the corkscrew project seems to be dead and the source code is only found in the big GNU/Linux distrubitions, I decided to rewrite it.

## Installation
You need to have `python` and `python-setuptools` installed. After that just run

    python setup.py install

## Usage
Usage is the same than in corkcrew

    langsax <proxyhost> <proxyport> <desthost> <destport> [authfile]

But this could change anytime at the moment.

