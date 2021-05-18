import argparse
import fnmatch
import yaml
import os
import re
import sys


parser = argparse.ArgumentParser(description='Find text between markdown YAML tags')
parser.add_argument('--extension', help='Extension of files to validate')
parser.add_argument('--directory', help='Path of directory to recursively go through')
args = parser.parse_args()

exit_status = 0

for root, dirs, files in os.walk(args.directory):
    for filename in fnmatch.filter(files, '*' + args.extension):
        with open(os.path.join(root, filename), "r") as validation_file:

            validation_data = validation_file.read()
            x = re.findall(r'{{< code yml >}}(.*?){{< /code >}}',
                           validation_data, re.DOTALL)

            for yaml_block in x:
                try:
                    yaml.loads(yaml_block)
                except ValueError as exception:
                    print "In file " + validation_file.name + " the following YAML is invalid\n" + \
                    str(exception) + "\n" + yaml_block + "\n"
                    exit_status = 2
sys.exit(exit_status)
