#!/usr/bin/python

ANSIBLE_METADATA = {
  'metadata_version': '1.1',
  'status': ['preview'],
  'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: decompress

short_description: This is a simple module for decompressing unarchived files

version_added: "2.4"

description:
    - "The module gets either a gz,bz2 or zip compressed file and just uncompress its content. Its purpose is to cover the case where a single file is just compressed such as a bootimage.iso.gz. but not archived. In case the file is archived, e.g. bootimage.tar.gz then the core module unarchive can handle it."

options:
    src:
        description:
            - This is the absolute path of the compressed file
        required: true
    dst:
        description:
            - The destination of the uncompressed file. This can be an absolute file path where the content will be saved as the specified filename, a directory where the filename will match the src filename without the (.gz|.bz2|.zip) extention or undefined. In the last case the file will be uncompressed in the same directory of the src with the same filename without the compress extention.
        required: false
    force:
        description:
            - Set this option to True to overwrite the extracted file in case it exists on destination.
        required: false
        default: false
    update:
        description:
            - Set this to True to overwrite the file only if it has different size/
        required: false
        default: true

extends_documentation_fragment:
    - files

author:
    - Socrates Chouridis
'''

EXAMPLES = '''
# This will decompress the bootimage.iso.gz and move it to ~/isos/bootimage.iso
- name: Decompress a gzipped iso image downloaded from the Internet
  decompress:
    src: '/tmp/bootimage.iso.gz'
    dest: '~/isos/'

# Setting the extracted file name explicitly
- name: Decompress a bz2 iso image downloaded from the Internet
  decompress:
    src: '/tmp/bootimage.iso.bz2'
    dest: '~/isos/newname_image.iso'

# Extract multiple images using with_items
- name: decompress multiple images
  decompress:
    src: "{{ item }}"
    dest: '/my-images/'
    force: true
  with_items: "{{ compressed_isos_list }}"

# Setting just the src will use the same name ommiting the extention, the result will be /tmp/bootimage.iso
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

from ansible.module_utils.basic import AnsibleModule
import gzip, shutil, posixpath, bz2, os, zipfile


def decompress_file(data={}):
  extensions = [".gz", ".bz2", ".zip"]
  try:
    original_file_path = str(
      posixpath.abspath(data['src'])
    )  # Original File  Absolute Path
    path_list = os.path.splitext(original_file_path)  # List
    original_file_dir = os.path.dirname(original_file_path)

    ext = path_list[1]

    destination = data['dst']

    force = data['force']
    update = data['update']

    if not destination:
      destination = path_list[0]
    elif not os.path.dirname(destination):
      destination = original_file_dir + "/" + destination
    elif not os.path.basename(destination):
      destination = destination + os.path.basename(path_list[0])

    if not os.path.exists(os.path.dirname(destination)):
      os.makedirs(os.path.dirname(destination), 755)

    extracted_filename = destination

    if os.path.isdir(destination):
      extracted_filename = path_list[0]
    if ext in extensions:
      if ext == ".gz":
        result = use_gzip(original_file_path, extracted_filename, force)
      elif ext == ".bz2":
        result = use_bzip2(original_file_path, extracted_filename, force)
      else:
        result = use_unzip(
          original_file_path, os.path.dirname(extracted_filename), force,
          update
        )
    else:
      message = "The file type " + "\"" + ext + "\"" + " is not supported by this module. Supported File Formats: .gz, .bz2, .zip"
      if ext == ".iso":
        message = "Supported File types: .gz, .bz2, .zip. Got .iso instead, perhaps the file is not compressed at all, ignoring... "
      return False, False, message, [original_file_path]

    return result[0], result[1], result[2], result[3]

  except Exception as e:
    message = "An error occurred. Decompress Failed: " + str(e)
    return True, False, message, {
      'Error': str(e)
    }


def use_gzip(src, dst, force):
  dst_exists = False
  if os.path.exists(dst):
    dst_exists = True

  with gzip.open(src, 'r') as f_in, open(dst, 'wb') as f_out:
    if not dst_exists:
      shutil.copyfileobj(f_in, f_out)
      message = "File Extracted Successfully: " + dst
      return False, True, message, [dst]
    else:
      if force:
        shutil.copyfileobj(f_in, f_out)
        message = "File Extracted Successfully and replaced file (Force = True): " + dst
        return False, True, message, [dst]
      else:
        message = "File Exists: skipping extraction (Use Force=True to Overwrite): " + dst
        return False, False, message, [dst]


def use_bzip2(src, dst, force):
  dst_exists = False
  if os.path.exists(dst):
    dst_exists = True
  with bz2.BZ2File(src, "r") as f_in, open(dst, "wb") as f_out:
    if not dst_exists:
      shutil.copyfileobj(f_in, f_out)
      message = "File Extracted Successfully: " + dst
      return False, True, message, [dst]
    else:
      if force:
        shutil.copyfileobj(f_in, f_out)
        message = "File Extracted Successfully and replaced file (Force = True): " + dst
        return False, True, message, [dst]
      else:
        message = "File Exists: skipping extraction (Use Force=True to Overwrite): " + dst
        return False, False, message, [dst]


def use_unzip(src, dst, force=False, update=True):
  filelist = []
  for root, dirs, files in os.walk(dst):
    for d in dirs:
      filelist.append(os.path.relpath(os.path.join(root, d), dst))
    for f in files:
      filelist.append(os.path.relpath(os.path.join(root, f), dst))

  extracted_files = []
  excluded_files = []
  with zipfile.ZipFile(src, 'r') as zip_file:
    for f in zip_file.namelist():
      print(os.path.relpath(f))
      if not os.path.relpath(f) in filelist:
        zip_file.extract(f, dst)
        extracted_files.append(f)
      else:
        if force:
          zip_file.extract(f, dst)
          extracted_files.append(f)
        else:
          info = zip_file.getinfo(f)
          if info.file_size != os.stat(dst + "/" + f).st_size:
            if update:
              zip_file.extract(f, dst)
              extracted_files.append(f)
            else:
              excluded_files.append(f)
          else:
            excluded_files.append(f)
  if not excluded_files:
    message = " All files were extracted successfully"
    for file in extracted_files:
      if not force and update and file in filelist:
        message = "Files with the same name on destination were replaced as they had different size (Update=True)"
      elif force:
        message = "All files were extracted successfully replacing any files on destination with the same name (Force=True)"
    return False, True, message, filelist
  else:
    if not extracted_files:
      message = "All Files Exist on Destination, Skipping Extraction... Use Force=True to Overwrite"
      return False, False, message, filelist
    else:
      message = "Some Files Skipped Extraction as they Existed on destination. Use Force=True to Overwrite "
      return False, True, message, filelist


def run_module():
  module_args = dict(
    src=dict(type='str', required=True),
    dst=dict(type='str', required=False),
    force=dict(type='bool', required=False, default=False),
    update=dict(type='bool', required=False, default=True),
  )

  result = dict(
    changed=False,
    message='',
    failed=False,
    files=[],
  )

  module = AnsibleModule(argument_spec=module_args)

  (error, is_changed, message, files) = decompress_file(module.params)

  result['changed'] = is_changed
  result['message'] = message
  result['failed'] = error
  result['files'] = files

  module.exit_json(**result)


def main():
  run_module()


if __name__ == '__main__':
  main()
