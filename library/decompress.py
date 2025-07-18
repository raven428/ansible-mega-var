ANSIBLE_METADATA = {
  'metadata_version': '1.1',
  'status': ['preview'],
  'supported_by': 'community',
}

DOCUMENTATION = '''
---
module: decompress

short_description: This is a simple module for decompressing unarchived files

version_added: "2.4"

description:
  - "The module gets either a gz,bz2 or zip compressed file and just uncompress its
    content. Its purpose is to cover the case where a single file is just compressed such
    as a bootimage.iso.gz. but not archived. In case the file is archived, e.g.
    bootimage.tar.gz then the core module unarchive can handle it."

options:
  src:
    description:
      - This is the absolute path of the compressed file
    required: true
  dst:
    description:
      - The destination of the uncompressed file. This can be an absolute file path where
        the content will be saved as the specified filename, a directory where the
        filename will match the src filename without the (.gz|.bz2|.zip) extention or
        undefined. In the last case the file will be uncompressed in the same directory
        of the src with the same filename without the compress extention.
    required: false
  force:
    description:
      - Set this option to True to overwrite the decompressed file in case it exists on
        destination.
    required: false
    default: false
  update:
    description:
      - Set this to True to overwrite the file only if it has different size
    required: false
    default: true

extends_documentation_fragment:
  - files

author:
  - Socrates Chouridis (https://github.com/socratesx/Ansible-Decompress)
  - Dmitry Sukhodoyev (https://github.com/raven428/ansible-mega-var)
'''

EXAMPLES = '''
# This will decompress the bootimage.iso.gz and move it to ~/isos/bootimage.iso
- name: Decompress a gzipped iso image downloaded from the Internet
  decompress:
    src: '/tmp/bootimage.iso.gz'
    dest: '~/isos/'

# Setting the decompressed file name explicitly
- name: Decompress a bz2 iso image downloaded from the Internet
  decompress:
    src: '/tmp/bootimage.iso.bz2'
    dest: '~/isos/newname_image.iso'

# Decompress multiple images using with_items
- name: Decompress multiple images
  decompress:
    src: "{{ item }}"
    dest: '/my-images/'
    force: true
  with_items: "{{ compressed_isos_list }}"

# Setting just the src will use the same name omiting the extention, the result will be
# /tmp/bootimage.iso
- name: Decompress in the same folder using the same name
  decompress:
    src: '/tmp/bootimage.iso.zip'
'''

RETURN = ''':
message:
    description: An information message regarding the decompression result.
    returned: 'always'
    type: 'str'
files:
    description: A list containing the files in the compressed file.
    returned: success
    type: list
'''

import importlib
import os
import posixpath
import shutil

# pylint: disable=import-error
from ansible.module_utils.basic import (  # type: ignore[reportMissingImports]
  AnsibleModule,
)


def decompress_file(data={}):  # noqa: ANN001,ANN201,B006,C901,PLR0912
  try:
    orig_file_path = str(posixpath.abspath(data['src']))
    path_list = os.path.splitext(orig_file_path)  # noqa: PTH122
    original_file_dir = os.path.dirname(orig_file_path)  # noqa: PTH120
    ext = path_list[1]
    destination = data['dst']
    force = data['force']
    if not destination:
      destination = path_list[0]
    elif not os.path.dirname(destination):  # noqa: PTH120
      destination = original_file_dir + '/' + destination
    elif not os.path.basename(destination):  # noqa: PTH119
      destination += os.path.basename(  # noqa: PTH119
        path_list[0],
      )
    if not os.path.exists(os.path.dirname(destination)):  # noqa: PTH110,PTH120
      os.makedirs(os.path.dirname(destination), 0o755)  # noqa: PTH103,PTH120
    dst = destination
    if os.path.isdir(destination):  # noqa: PTH112
      dst = path_list[0]
    dst_exists = os.path.exists(dst)  # noqa: PTH110
    result = []
    if dst_exists and not force:
      result = [
        False,
        False,
        'File [' + dst +
        '] exists: skipping decompression. Use Force: true to overwrite)',
        dst,
      ]
    elif ext in {'.xz', '.lzma'}:
      lzma = importlib.import_module('lzma')

      with lzma.open(orig_file_path,
                     'r') as f_in, open(dst, 'wb') as f_out:  # noqa: PTH123
        shutil.copyfileobj(f_in, f_out)
    elif ext == '.gz':
      gzip = importlib.import_module('gzip')
      with gzip.open(orig_file_path,
                     'r') as f_in, open(dst, 'wb') as f_out:  # noqa: PTH123
        shutil.copyfileobj(f_in, f_out)
    elif ext == '.bz2':
      bz2 = importlib.import_module('bz2')
      with bz2.BZ2File(orig_file_path,
                       'r') as f_in, open(dst, 'wb') as f_out:  # noqa: PTH123
        shutil.copyfileobj(f_in, f_out)
    elif ext in {'.zst', '.zstd'}:
      zstd = importlib.import_module('zstd')
      with open(  # noqa: PTH123,FURB101
        orig_file_path,
        'rb',
      ) as f_in, open(dst, 'wb') as f_out:  # noqa: PTH123,FURB103
        f_out.write(zstd.decompress(f_in.read()))
    elif ext == '.lz4':
      lz4 = importlib.import_module('lz4.frame')
      with open(  # noqa: PTH123,FURB101
        orig_file_path,
        'rb',
      ) as f_in, open(dst, 'wb') as f_out:  # noqa: PTH123,FURB103
        f_out.write(lz4.decompress(f_in.read()))
    else:
      result = [
        True,
        False,
        'The file type [' + ext + '] is not supported by this module. ' +
        'Supported file formats are .xz .gz, .bz2 .lzma .lz .lzip ' + '.zst .zstd .lz4',
        orig_file_path,
      ]
    if result == []:
      result = [
        False,
        True,
        'File decompressed successfully' +
        (' and replaced because Force: true' if dst_exists else '') + ': ' + dst,
        dst,
      ]
    return result[0], result[1], result[2], result[3]
  except Exception as e:  # noqa: BLE001
    message = f'Error {e} occurred'
    return True, False, message, {
      'Error': str(e),
    }


def run_module() -> None:
  module_args = {
    'src': {
      'type': 'str',
      'required': True,
    },
    'dst': {
      'type': 'str',
      'required': False,
    },
    'force': {
      'type': 'bool',
      'required': False,
      'default': False,
    },
    'update': {
      'type': 'bool',
      'required': False,
      'default': True,
    },
  }
  module = AnsibleModule(argument_spec=module_args)
  (error, is_changed, message, files) = decompress_file(module.params)
  result = {
    'changed': is_changed,
    'message': message,
    'failed': error,
    'files': files,
  }
  module.exit_json(**result)


def main() -> None:
  run_module()


if __name__ == '__main__':
  main()
