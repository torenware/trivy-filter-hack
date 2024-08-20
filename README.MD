## Deploying The Trivy Hack

This repo contains a "proof of concept" of how to get around trivy's over-eagarness to pull from Docker Hub. It works because trivy as currently coded (v0.54) will check a docker server if it is present for any image trivy is asked for in `trivy image` *before* it attempts to go to the network to load the image from a remote source. Since trivy does not respect docker's mirroring settings, the code in this repo does the following tricks:

* We put a small bash script in front of the real trivy comand (called "fake trivy" below) to check if "trivy image" is being called.  If it isn't, we exec real trivy.
* If it *is* a `trivy image` call, we call a small python program that does the following:
  + Parse the trivy image command and its arguments.
  + Checks the local docker server for the requested image, and pulls the image if it is absent.
  + Returns the full command that calls real trivy to the fake trivy script.

Since the local docker server can be configured to use mirroring, this gets around the too-many-requests issue.

### How to use the files

On any lab container that uses trivy, do the following:

1. Install docker-ce and python3-pip
2. Run `pip3 install docker` to install the python docker library.
3. Copy trivy-wrap.py somewhere on the image (I'll put it in /usr/local/bin/ as the location for this example).
4. Copy settings.py to the same directory as trivy-wrap.py and edit it to point to the actual trivy binary (this is currently /usr/bin/trivy on the containers I've checked).
5. Edit rewrite.sh to point to trivy-wrap.py and install it as /usr/local/bin/trivy.

This has worked in my tests. It's unnecessary to use the "long form" image names, since trivy will load the normal short names w/o a problem using the trivy-wrap.py script.
