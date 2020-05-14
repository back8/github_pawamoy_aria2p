#!/usr/bin/env python
"""Regenerate all templated documentation pages."""

import sys
from pathlib import Path

import requests
from gen_credits_data import get_data as get_credits
from gen_readme_data import get_data as get_readme
from jinja2 import StrictUndefined
from jinja2.exceptions import TemplateError
from jinja2.sandbox import SandboxedEnvironment

URL_PREFIX = "https://raw.githubusercontent.com/pawamoy/jinja-templates/master/"
REGEN = [
    ("docs/credits.md", get_credits, URL_PREFIX + "credits.md"),
    ("docs/index.md", get_readme, "scripts/templates/README.md"),
]


def main():
    """Regenerate pages listed in global `REGEN` list."""
    env = SandboxedEnvironment(undefined=StrictUndefined)
    for target, get_data, template in REGEN:
        print("Regenerating", target)
        data = get_data()
        if Path(template).exists():
            with open(template) as fd:
                template_text = fd.read()
        else:
            template_text = requests.get(template).text
        try:
            rendered = env.from_string(template_text).render(**data)
        except TemplateError as error:
            print("Error while regenerating", target)
            print(error)
            return 1
        with open(target, "w") as target:
            target.write(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
