#!/usr/bin/env python

import argparse
import json

from aria2p.cli import get_parser


def get_data():
    """Return data used to generate the credits file."""
    parser = get_parser()
    aliases = [
        "add-magnet",
        "add-metalink",
        "add-torrent",
        "autoclear",
        "clear",
        "rm",
        "del",
        "delete",
        "start",
        "stop",
    ]
    output = {"main_usage": parser.format_help(), "commands": []}
    subparser_actions = [action for action in parser._actions if isinstance(action, argparse._SubParsersAction)]

    for subparser_action in subparser_actions:
        for choice, subparser in subparser_action.choices.items():
            if choice in aliases:
                continue
            output["commands"].append({"name": choice, "usage": subparser.format_help()})

    output["commands"] = list(sorted(output["commands"], key=lambda c: c["name"]))
    return output


def main():
    """Dump data as JSON."""
    print(json.dumps(get_data()))


if __name__ == "__main__":
    main()
