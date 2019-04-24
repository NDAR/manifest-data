import os
import sys
import json
import hashlib
import argparse

"""
Utilities in python for working with NDA Manifests.
1. Create a python object that represents an NDA Manifest from either a json manifest file, or a directory structure
2. Output an NDA Manifest as either JSON string or as a JSON file
3. Materialize an NDA Manifest, creates directory structure and fake files; useful for testing/debugging.
"""


class ManifestRecord:

    """
    Represents an individual record within a manifest file.

    Initialized with either:
     * filepath (create from a real file)
     * dictionary representing a manifest record
    """

    def __init__(self, file):
        try:
            self.from_file(file)
        except TypeError:
            self.path = file['path']
            self.name = file['name']
            self.size = file['size']
            self.md5sum = file['md5sum']

    def from_file(self, file):
        self.path = file
        self.name = os.path.basename(file)
        self.size = os.path.getsize(file)
        self.md5sum = self.md5(file)

    @staticmethod
    def md5(file):
        digest = hashlib.md5()
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                digest.update(chunk)
        return digest.hexdigest()


class Manifest:

    """
    Class representing an NDA Manifest

    Initialized as just an empty list, with methods for adding records:
     * from a directory structure (adds all directories/files recursively)
     * from a manifest json file

    Output methods for manifest to:
     * json string
     * json file
     * directory structure and files that represent the manifests contents
    """

    def __init__(self):
        self.files = []

    def materialize(self):
        for manifest_record in self.files:
            try:
                path = os.path.join(args.output_dir, manifest_record.path)
                os.makedirs(os.path.dirname(path))
            except FileExistsError:
                pass
            json.dump(vars(manifest_record),
                      open(path, "w+"))

    def create_from_dir(self, directory):
        for (path, dirnames, filenames) in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(path, filename)
                self.files.append(ManifestRecord(file_path))

    def create_from_json_file(self, fp):
        try:
            for file in json.load(fp)['files']:
                self.files.append(ManifestRecord(file))
        except AttributeError:
            self.files = None
        except json.decoder.JSONDecodeError:
            print('Error decoding file {}, check that it is valid JSON.'.format(fp.name))
            self.files = None
        except KeyError:
            print('Check that your file {} conforms to the expected schema.'.format(fp.name))
            self.files = None

    def output_as_file(self, filename):
        json.dump(json.loads(self.output_as_json), open(filename, 'w+'))

    @property
    def output_as_json(self):
        output = {'files': []}
        for manifest_record in self.files:
            output['files'].append(vars(manifest_record))
        return json.dumps(output)


def load_args():
    parser = argparse.ArgumentParser(description='Create a Manifest File from a directory '
                                                 'or a directory from a Manifest file.')
    input_file_group = parser.add_mutually_exclusive_group()
    input_dir_group = parser.add_mutually_exclusive_group()
    input_file_group.add_argument('-if', '--input-file',
                                  help='A Manifest File in JSON format as input, to create a directory from.')
    input_file_group.add_argument('-id', '--input-dir',
                                  help='A directory as input, to create a Manifest File from.')
    input_dir_group.add_argument('-of', '--output-file', default=os.path.join(os.curdir,'output_file.json'),
                                 help='A Manifest File in JSON format, created from an input directory.')
    input_dir_group.add_argument('-od', '--output-dir', default=os.path.join(os.curdir,'OutputDir'),
                                 help='An directory as output, created from a Manifest File')
    args = parser.parse_args()

    if args.input_file is None and args.input_dir is None:
        parser.error('No input specified, must have one input type, --input_file or --input_dir')
    return args


if __name__ == "__main__":

    args = load_args()
    if args.input_dir and os.path.isdir(args.input_dir):
        print('Creating a manifest file from a directory tree {}'.format(args.input_dir))
        new_manifest = Manifest()
        new_manifest.create_from_dir(args.input_dir)
        new_manifest.output_as_file(args.output_file)
        print(new_manifest.output_as_json)

    elif args.input_file and os.path.isfile(args.input_file):
        with open(args.input_file, 'r') as json_file:
            manifest = Manifest()
            manifest.create_from_json_file(json_file)
            manifest.materialize()