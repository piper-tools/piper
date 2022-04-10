import argparse
import importlib
import inspect
import sys
from pathlib import Path

import yaml
from piperblue.blueprint import PiperBlueprint


def _find(yml, bag):
    try:
        for b, properties in yml.items():
            if b == bag:
                return properties
            found = _find(yml[b], bag)
            if found:
                return found
    except:
        return None


def _generate(file: str, blueprint_name: str, bag: str, context: str):

    # Find the config
    with open(file) as f:
        yml = yaml.load(f, Loader=yaml.SafeLoader)
    properties = _find(yml, bag)
    config = properties.get("config")

    # Import the blueprint class
    module = f"{blueprint_name}.blueprint"
    all_blueprints = inspect.getmembers(
        importlib.import_module(module),
        lambda member: inspect.isclass(member) and member.__module__ == module and issubclass(member, PiperBlueprint)
    )[0]
    blueprint = all_blueprints[1]

    # Get its resources folder
    resources_folder = str(Path(sys.modules[blueprint.__module__].__file__).parent / "resources")

    # Instantiate it and run it
    blueprint().generate(resources_folder, context, config)


def main():

    # Parse
    parser = argparse.ArgumentParser()
    parser.add_argument("--file")
    parser.add_argument("--context")
    parser.add_argument("--bag")
    parser.add_argument("--blueprint")
    args = parser.parse_args()

    # Generate
    _generate(args.file, args.blueprint, args.bag, args.context)


if __name__ == '__main__':

    main()
