import os

from utils import configurations


def config(args):
    if args.collection:
        configurations.set_collection(args.collection)


def update(args):
    if os.path.exists(args.text):
        text = open(args.text, "r")
    else:
        text = [args.text]
