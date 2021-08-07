from setuptools import setup, find_packages
import os


# Function to retrieve resources files
def _get_resources(package_name):
    # Get all the resources (also on nested levels)
    res_paths = os.path.join(package_name, "resources")
    all_resources = [os.path.join(folder, file) for folder, _, files in os.walk(res_paths) for file in files]
    # Remove the prefix: start just from "resources"
    return [resource[resource.index("resources"):] for resource in all_resources]


# Read requirements
requirements_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")
with open(requirements_file, "r") as f:
    requirements = f.read().splitlines()


# Package configuration
setup(
    name="piper",
    version="0.0.0",
    description="A Snake Charmer to manage you Python code",
    packages=find_packages(),
    package_data={"piper": _get_resources("piper")},
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'piper = piper.__main__:main',
        ],
    },
)
