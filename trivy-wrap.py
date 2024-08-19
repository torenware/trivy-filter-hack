#! /usr/bin/env python3

import sys
import argparse
import docker

TRIVY = "/usr/local/bin/trivy"
client = docker.from_env()


def pull_image(repo, tag):
    client.images.pull(repo, tag)


def ensure_image(repo, tag):
    path = "%s:%s" % (repo, tag)
    tags = [path for img in client.images.list(
        name='nginx') for path in img.tags]
    if path not in tags:
        pull_image(repo, tag)


def build_command():

    parser = argparse.ArgumentParser()

    parser.add_argument("keyword", help="subcommand", type=str)
    parser.add_argument("image", help="Image to parse", type=str)
    parser.add_argument("-s", "--severity", help="serverity to list",
                        type=str)

    args = parser.parse_known_args()
    ns = args[0]
    rest = args[1]
    cmd = "trivy image " + ns.image

    if ns.severity:
        cmd += " -s " + ns.severity

    if len(rest) > 0:
        cmd += ' '.join(rest)

    return (cmd, ns.image)


def expand_image(image):
    """
    normalize an image name
    """
    tagged = image.split(':')
    tag = 'latest'
    if len(tagged) == 2:
        tag = tagged[1]
    elif len(tagged) > 2:
        print("badly formed image name", file=sys.stderr)
        exit(1)

    registry = 'docker.io'
    owner = 'library'
    names = tagged[0].split('/')
    if len(names) > 3:
        print("badly formed image name", file=sys.stderr)
        exit(1)

    if len(names) == 3:
        registry = names[0]
        owner = names[1]
    elif len(names) == 2:
        owner = names[0]

    repo = names[-1]
    full_repo = image.split(':')[0]
    ensure_image(full_repo, tag)

    full_image = "%s/%s/%s:%s" % (registry, owner, repo, tag)
    short_image = "%s:%s" % (repo, tag)
    return (full_image, short_image)


if __name__ == '__main__':
    # Execute when the module is not initialized from an import statement.
    cmd, img = build_command()
    full, short = expand_image(img)
    print(cmd)
