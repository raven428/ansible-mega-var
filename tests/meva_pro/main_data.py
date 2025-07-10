# flake8: noqa: S108
mock_dirs_list = [
  "/tmp/ansible-controller_copy_000.tar.xz-dir/pyenv/bin",
  "/tmp/ansible-controller_copy_000.tar.xz-dir/pyenv/pyenv.d/install",
]
cases_resolve_paths = [
  {
    "i_dest": "/tmp/molecule",
    "f_dest": "",
    "f_name": "pyenv/bin/",
    "f_src": "",
    "src_dir": "/tmp/ansible-controller_copy_000.tar.xz-dir",
    "dest4copy": "/tmp/molecule/pyenv/bin/",
    "dest4dir": "",
    "dest4path": "/tmp/molecule/pyenv/bin/",
    "src4copy": "/tmp/ansible-controller_copy_000.tar.xz-dir/pyenv/bin/",
    "src_is_dir": True
  },
  {
    "i_dest": "/tmp/molecule",
    "f_dest": "",
    "f_name": "pyenv/Makefile",
    "f_src": "",
    "src_dir": "/tmp/ansible-controller_copy_000.tar.xz-dir",
    "dest4copy": "/tmp/molecule/pyenv/Makefile",
    "dest4dir": "/tmp/molecule/pyenv",
    "dest4path": "/tmp/molecule/pyenv/Makefile",
    "src4copy": "/tmp/ansible-controller_copy_000.tar.xz-dir/pyenv/Makefile",
    "src_is_dir": False
  },
  {
    "i_dest": "/tmp/molecule",
    "f_dest": "",
    "f_name": "pyenv/pyenv.d/install",
    "f_src": "",
    "src_dir": "/tmp/ansible-controller_copy_000.tar.xz-dir",
    "dest4copy": "/tmp/molecule/pyenv/pyenv.d/install/",
    "dest4dir": "",
    "dest4path": "/tmp/molecule/pyenv/pyenv.d/install",
    "src4copy": "/tmp/ansible-controller_copy_000.tar.xz-dir/pyenv/pyenv.d/install",
    "src_is_dir": True
  },
  {
    "i_dest": "/tmp/molecule",
    "f_dest": "/tmp/molecule//absolute-f.dest-no",
    "f_name": "pyenv/bin",
    "f_src": "",
    "src_dir": "/tmp/ansible-controller_copy_000.tar.xz-dir",
    "dest4copy": "/tmp/molecule//absolute-f.dest-no/",
    "dest4dir": "",
    "dest4path": "/tmp/molecule//absolute-f.dest-no",
    "src4copy": "/tmp/ansible-controller_copy_000.tar.xz-dir/pyenv/bin",
    "src_is_dir": True
  },
  {
    "i_dest": "/tmp/molecule",
    "f_dest": "/tmp/molecule//absolute-f.dest-trailing-slash-no",
    "f_name": "pyenv/bin/",
    "f_src": "",
    "src_dir": "/tmp/ansible-controller_copy_000.tar.xz-dir",
    "dest4copy": "/tmp/molecule//absolute-f.dest-trailing-slash-no/",
    "dest4dir": "",
    "dest4path": "/tmp/molecule//absolute-f.dest-trailing-slash-no",
    "src4copy": "/tmp/ansible-controller_copy_000.tar.xz-dir/pyenv/bin/",
    "src_is_dir": True
  },
  {
    "i_dest": "/tmp/molecule",
    "f_dest": "/tmp/molecule/absolute-f.dest-trailing-slash-yes/",
    "f_name": "pyenv/bin/",
    "f_src": "",
    "src_dir": "/tmp/ansible-controller_copy_000.tar.xz-dir",
    "dest4copy": "/tmp/molecule/absolute-f.dest-trailing-slash-yes/",
    "dest4dir": "",
    "dest4path": "/tmp/molecule/absolute-f.dest-trailing-slash-yes",
    "src4copy": "/tmp/ansible-controller_copy_000.tar.xz-dir/pyenv/bin/",
    "src_is_dir": True
  },
  {
    "i_dest": "/tmp/molecule",
    "f_dest": "/tmp/molecule/absolute-f.dest-trailing-yes/",
    "f_name": "pyenv/bin",
    "f_src": "",
    "src_dir": "/tmp/ansible-controller_copy_000.tar.xz-dir",
    "dest4copy": "/tmp/molecule/absolute-f.dest-trailing-yes/",
    "dest4dir": "",
    "dest4path": "/tmp/molecule/absolute-f.dest-trailing-yes/bin",
    "src4copy": "/tmp/ansible-controller_copy_000.tar.xz-dir/pyenv/bin",
    "src_is_dir": True
  },
  {
    "i_dest": "/tmp/molecule",
    "f_dest": "/tmp/molecule/f.dest-abs1/",
    "f_name": "pyenv/Makefile",
    "f_src": "",
    "src_dir": "/tmp/ansible-controller_copy_000.tar.xz-dir",
    "dest4copy": "/tmp/molecule/f.dest-abs1/",
    "dest4dir": "",
    "dest4path": "/tmp/molecule/f.dest-abs1/Makefile",
    "src4copy": "/tmp/ansible-controller_copy_000.tar.xz-dir/pyenv/Makefile",
    "src_is_dir": False
  },
  {
    "i_dest":
      "/tmp/molecule",
    "f_dest":
      "/tmp/molecule/f.dest-abs2/file-default.list",
    "f_name":
      "pyenv/pyenv.d/rehash/conda.d/default.list",
    "f_src":
      "",
    "src_dir":
      "/tmp/ansible-controller_copy_000.tar.xz-dir",
    "dest4copy":
      "/tmp/molecule/f.dest-abs2/file-default.list",
    "dest4dir":
      "/tmp/molecule/f.dest-abs2",
    "dest4path":
      "/tmp/molecule/f.dest-abs2/file-default.list",
    "src4copy":
      "/tmp/ansible-controller_copy_000.tar.xz-dir/pyenv/pyenv.d/rehash/conda.d/default.list",
    "src_is_dir":
      False
  },
  {
    "i_dest": "/tmp/molecule",
    "f_dest": "f.dest-dir1/",
    "f_name": "pyenv/Makefile",
    "f_src": "",
    "src_dir": "/tmp/ansible-controller_copy_000.tar.xz-dir",
    "dest4copy": "/tmp/molecule/f.dest-dir1/",
    "dest4dir": "",
    "dest4path": "/tmp/molecule/f.dest-dir1/Makefile",
    "src4copy": "/tmp/ansible-controller_copy_000.tar.xz-dir/pyenv/Makefile",
    "src_is_dir": False
  },
  {
    "i_dest": "/tmp/molecule",
    "f_dest": "f.dest-dir2/in-f.dest-Makefile",
    "f_name": "pyenv/Makefile",
    "f_src": "",
    "src_dir": "/tmp/ansible-controller_copy_000.tar.xz-dir",
    "dest4copy": "/tmp/molecule/f.dest-dir2/in-f.dest-Makefile",
    "dest4dir": "/tmp/molecule/f.dest-dir2",
    "dest4path": "/tmp/molecule/f.dest-dir2/in-f.dest-Makefile",
    "src4copy": "/tmp/ansible-controller_copy_000.tar.xz-dir/pyenv/Makefile",
    "src_is_dir": False
  },
  {
    "i_dest": "/tmp/molecule",
    "f_dest": "relative-f.dest-trailing-no",
    "f_name": "pyenv/bin",
    "f_src": "",
    "src_dir": "/tmp/ansible-controller_copy_000.tar.xz-dir",
    "dest4copy": "/tmp/molecule/relative-f.dest-trailing-no/",
    "dest4dir": "",
    "dest4path": "/tmp/molecule/relative-f.dest-trailing-no",
    "src4copy": "/tmp/ansible-controller_copy_000.tar.xz-dir/pyenv/bin",
    "src_is_dir": True
  },
  {
    "i_dest": "/tmp/molecule",
    "f_dest": "relative-f.dest-trailing-slash-no",
    "f_name": "pyenv/bin/",
    "f_src": "",
    "src_dir": "/tmp/ansible-controller_copy_000.tar.xz-dir",
    "dest4copy": "/tmp/molecule/relative-f.dest-trailing-slash-no/",
    "dest4dir": "",
    "dest4path": "/tmp/molecule/relative-f.dest-trailing-slash-no",
    "src4copy": "/tmp/ansible-controller_copy_000.tar.xz-dir/pyenv/bin/",
    "src_is_dir": True
  },
  {
    "i_dest": "/tmp/molecule",
    "f_dest": "relative-f.dest-trailing-slash-yes/",
    "f_name": "pyenv/bin/",
    "f_src": "",
    "src_dir": "/tmp/ansible-controller_copy_000.tar.xz-dir",
    "dest4copy": "/tmp/molecule/relative-f.dest-trailing-slash-yes/",
    "dest4dir": "",
    "dest4path": "/tmp/molecule/relative-f.dest-trailing-slash-yes",
    "src4copy": "/tmp/ansible-controller_copy_000.tar.xz-dir/pyenv/bin/",
    "src_is_dir": True
  },
  {
    "i_dest": "/tmp/molecule",
    "f_dest": "relative-f.dest-trailing-yes/",
    "f_name": "pyenv/bin",
    "f_src": "",
    "src_dir": "/tmp/ansible-controller_copy_000.tar.xz-dir",
    "dest4copy": "/tmp/molecule/relative-f.dest-trailing-yes/",
    "dest4dir": "",
    "dest4path": "/tmp/molecule/relative-f.dest-trailing-yes/bin",
    "src4copy": "/tmp/ansible-controller_copy_000.tar.xz-dir/pyenv/bin",
    "src_is_dir": True
  },
  {
    "i_dest": "/tmp/molecule/bz2",
    "f_dest": "",
    "f_name": "decompressed-file-name",
    "f_src": "/tmp/ansible-decompressed_file_name.bz2-dir/decompressed-file-name",
    "src_dir": "/tmp/ansible-decompressed_file_name.bz2-dir",
    "dest4copy": "/tmp/molecule/bz2/decompressed-file-name",
    "dest4dir": "/tmp/molecule/bz2",
    "dest4path": "/tmp/molecule/bz2/decompressed-file-name",
    "src4copy": "/tmp/ansible-decompressed_file_name.bz2-dir/decompressed-file-name",
    "src_is_dir": False
  },
  {
    "i_dest": "/tmp/molecule/compress/controller-copy",
    "f_dest": "",
    "f_name": "decompressed-file-name",
    "f_src": "/tmp/ansible-compress_controller_copy.xz-dir/decompressed-file-name",
    "src_dir": "/tmp/ansible-compress_controller_copy.xz-dir",
    "dest4copy": "/tmp/molecule/compress/controller-copy/decompressed-file-name",
    "dest4dir": "/tmp/molecule/compress/controller-copy",
    "dest4path": "/tmp/molecule/compress/controller-copy/decompressed-file-name",
    "src4copy": "/tmp/ansible-compress_controller_copy.xz-dir/decompressed-file-name",
    "src_is_dir": False
  },
  {
    "i_dest": "/tmp/molecule/compress/direct-download",
    "f_dest": "",
    "f_name": "decompressed-file-name",
    "f_src": "/tmp/ansible-compress_direct_download.xz-dir/decompressed-file-name",
    "src_dir": "/tmp/ansible-compress_direct_download.xz-dir",
    "dest4copy": "/tmp/molecule/compress/direct-download/decompressed-file-name",
    "dest4dir": "/tmp/molecule/compress/direct-download",
    "dest4path": "/tmp/molecule/compress/direct-download/decompressed-file-name",
    "src4copy": "/tmp/ansible-compress_direct_download.xz-dir/decompressed-file-name",
    "src_is_dir": False
  },
  {
    "i_dest": "/tmp/molecule/gz",
    "f_dest": "",
    "f_name": "decompressed-file-name",
    "f_src": "/tmp/ansible-decompressed_file_name.gz-dir/decompressed-file-name",
    "src_dir": "/tmp/ansible-decompressed_file_name.gz-dir",
    "dest4copy": "/tmp/molecule/gz/decompressed-file-name",
    "dest4dir": "/tmp/molecule/gz",
    "dest4path": "/tmp/molecule/gz/decompressed-file-name",
    "src4copy": "/tmp/ansible-decompressed_file_name.gz-dir/decompressed-file-name",
    "src_is_dir": False
  },
  {
    "i_dest": "/tmp/molecule/lz4",
    "f_dest": "",
    "f_name": "decompressed-file-name",
    "f_src": "/tmp/ansible-decompressed_file_name.lz4-dir/decompressed-file-name",
    "src_dir": "/tmp/ansible-decompressed_file_name.lz4-dir",
    "dest4copy": "/tmp/molecule/lz4/decompressed-file-name",
    "dest4dir": "/tmp/molecule/lz4",
    "dest4path": "/tmp/molecule/lz4/decompressed-file-name",
    "src4copy": "/tmp/ansible-decompressed_file_name.lz4-dir/decompressed-file-name",
    "src_is_dir": False
  },
  {
    "i_dest": "/tmp/molecule/lzma",
    "f_dest": "",
    "f_name": "decompressed-file-name",
    "f_src": "/tmp/ansible-decompressed_file_name.lzma-dir/decompressed-file-name",
    "src_dir": "/tmp/ansible-decompressed_file_name.lzma-dir",
    "dest4copy": "/tmp/molecule/lzma/decompressed-file-name",
    "dest4dir": "/tmp/molecule/lzma",
    "dest4path": "/tmp/molecule/lzma/decompressed-file-name",
    "src4copy": "/tmp/ansible-decompressed_file_name.lzma-dir/decompressed-file-name",
    "src_is_dir": False
  },
  {
    "i_dest":
      "/tmp/molecule/single/controller-copy",
    "f_dest":
      "",
    "f_name":
      "pyenv-emtpy-2_2_4-linux-amd64.tar.xz",
    "f_src":
      "/tmp/ansible-single_controller_copy.xz",
    "src_dir":
      "/tmp/ansible-single_controller_copy.xz-dir",
    "dest4copy":
      "/tmp/molecule/single/controller-copy/pyenv-emtpy-2_2_4-linux-amd64.tar.xz",
    "dest4dir":
      "/tmp/molecule/single/controller-copy",
    "dest4path":
      "/tmp/molecule/single/controller-copy/pyenv-emtpy-2_2_4-linux-amd64.tar.xz",
    "src4copy":
      "/tmp/ansible-single_controller_copy.xz",
    "src_is_dir":
      False
  },
  {
    "i_dest":
      "/tmp/molecule/single/direct-download",
    "f_dest":
      "",
    "f_name":
      "pyenv-emtpy-2_2_4-linux-amd64.tar.xz",
    "f_src":
      "/tmp/ansible-single_direct_download.xz",
    "src_dir":
      "/tmp/molecule/single/direct-download",
    "dest4copy":
      "/tmp/molecule/single/direct-download/pyenv-emtpy-2_2_4-linux-amd64.tar.xz",
    "dest4dir":
      "/tmp/molecule/single/direct-download",
    "dest4path":
      "/tmp/molecule/single/direct-download/pyenv-emtpy-2_2_4-linux-amd64.tar.xz",
    "src4copy":
      "/tmp/ansible-single_direct_download.xz",
    "src_is_dir":
      False
  },
  {
    "i_dest": "/tmp/molecule/xz",
    "f_dest": "",
    "f_name": "decompressed-file-name",
    "f_src": "/tmp/ansible-decompressed_file_name.xz-dir/decompressed-file-name",
    "src_dir": "/tmp/ansible-decompressed_file_name.xz-dir",
    "dest4copy": "/tmp/molecule/xz/decompressed-file-name",
    "dest4dir": "/tmp/molecule/xz",
    "dest4path": "/tmp/molecule/xz/decompressed-file-name",
    "src4copy": "/tmp/ansible-decompressed_file_name.xz-dir/decompressed-file-name",
    "src_is_dir": False
  },
  {
    "i_dest": "/tmp/molecule/zst",
    "f_dest": "",
    "f_name": "decompressed-file-name",
    "f_src": "/tmp/ansible-decompressed_file_name.zst-dir/decompressed-file-name",
    "src_dir": "/tmp/ansible-decompressed_file_name.zst-dir",
    "dest4copy": "/tmp/molecule/zst/decompressed-file-name",
    "dest4dir": "/tmp/molecule/zst",
    "dest4path": "/tmp/molecule/zst/decompressed-file-name",
    "src4copy": "/tmp/ansible-decompressed_file_name.zst-dir/decompressed-file-name",
    "src_is_dir": False
  },
]
