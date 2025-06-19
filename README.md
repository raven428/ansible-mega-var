# Actions from inventory variables

[![molecule](https://github.com/raven428/ansible-mega-var/actions/workflows/test-role.yaml/badge.svg)](https://github.com/raven428/ansible-mega-var/actions/workflows/test-role.yaml)

The role performs actions from inventory variables without creating a lot of tasks and copy-pasted roles

## Example `site.yaml` (TLDR)

### For the whole role

In case you have most of the variables filled it's

```yaml
- name: Perform some files, dirs, and templates upload
  hosts: mega_var
  become: true
  handlers:
    - import_tasks: handlers/main.yaml
  roles:
    - role: mega-var
      vars:
        meva_packages: "{{ meva_site_packages }}"
        meva_groups2create: "{{ meva_site_groups2create }}"
        meva_users2create: "{{ meva_site_users2create }}"
        meva_dirs2create: "{{ meva_site_dirs2create }}"
        meva_templates2upload: "{{ meva_site_templates2upload }}"
        meva_files2upload: "{{ meva_site_files2upload }}"
        meva_content2upload: "{{ meva_site_content2upload }}"
        meva_tree2rsync: "{{ meva_site_tree2rsync }}"
        meva_systemd4units: "{{ meva_site_systemd4units }}"
        meva_key2user: "{{ meva_site_key2user }}"
        meva_file2down: "{{ meva_site_file2down }}"
        meva_partitions: "{{ meva_site_partitions }}"
        meva_lvg: "{{ meva_site_lvg }}"
        meva_lvol: "{{ meva_site_lvol }}"
        meva_filesystems: "{{ meva_site_filesystems }}"
        meva_mounts: "{{ meva_site_mounts }}"
        meva_ghr2down: "{{ meva_site_ghr2down }}"
        meva_file2down: "{{ meva_site_file2down }}"
  tags: [mega-var]
```

### By separate calls

In case you haven't filled most of the variables, the role call can be significantly speed up. Simple by using `tasks_from:` directive:

```yaml
- name: Separate mega-var calls examples
  hosts: mega_var
  become: true
  handlers:
    - import_tasks: handlers/main.yaml
  tasks:
    - name: Install some packages outside of the whole role call
      ansible.builtin.include_role:
        role: mega-var
        tasks_from: _apt.yaml
      vars:
        meva_packages: "{{ meva_site_packages }}"
    - name: Ensure some groups outside of the whole role call
      ansible.builtin.include_role:
        role: mega-var
        tasks_from: _group.yaml
      vars:
        meva_groups2create: "{{ meva_site_groups2create }}"
    - name: Ensure some users outside of the whole role call
      ansible.builtin.include_role:
        role: mega-var
        tasks_from: _user.yaml
      vars:
        meva_users2create: "{{ meva_site_users2create }}"
    - name: Ensure some dirs outside of the whole role call
      ansible.builtin.include_role:
        role: mega-var
        tasks_from: _dir.yaml
      vars:
        meva_dirs2create: "{{ meva_site_dirs2create }}"
    - name: Ensure some templates outside of the whole role call
      ansible.builtin.include_role:
        role: mega-var
        tasks_from: _template.yaml
      vars:
        meva_templates2upload: "{{ meva_site_templates2upload }}"
    - name: Ensure some files outside of the whole role call
      ansible.builtin.include_role:
        role: mega-var
        tasks_from: _file.yaml
      vars:
        meva_files2upload: "{{ meva_site_files2upload }}"
- name: Download some files from GitHub releases example
  hosts: download_github
  become: true
  handlers:
    - import_tasks: handlers/main.yaml
  tasks:
    - name: Download some files from GitHub releases
      ansible.builtin.include_role:
        role: mega-var
        tasks_from: _download.yaml
      loop_control:
        loop_var: i
      loop: "{{ meva_site_ghr2down }}"
```

## Role variables description

All the variables except `meva_ghr2down` and `meva_file2down` is just wrapper and refers to according Ansible module documentation. Most keys of `meva_ghr2down` and `meva_file2down` variables also refers to `ansible.builtin.get_url` documentation

Here will be only non-obvious options of usage

### Simple HTTP download with `meva_file2down` variable

There are [the molecule tests](molecule/downloads/group_vars/all.yaml) cases description. Most options are available from `ansible.builtin.get_url`, `ansible.builtin.file` and `ansible.builtin.copy`

#### Single raw download (remote and local)

Cases `1.1.1` and `1.1.2`:

```yaml
- url: "http://url.to/download.ext"
  dest: "/dir/on/target/host/with/filename.ext"
  delegate_to: localhost
```

With `delegate_to` is set either to `localhost` or `127.0.0.1` file from `url` will be downloaded to Ansible controller first. Then `ansible.builtin.copy` will spread file to destination hosts. This can be useful when `url` source isn't able to handle a lot of requests from hosts in configuration

#### Single compressed download to remote

Case `1.2.1`:

```yaml
- url: "http://url.to/download.ext.gz"
  dest: "/dir/on/target/host/with/"
  creates: "filename.ext"
  archive: true
```

This option will decompress downloaded file. Parameter `dest` should contain the destination directory name only, without a filename.

Filename part of the decompressed file separated to `creates` key. The `archive: true` indicates that downloaded file should be decompressed extension from `uri`. Extension `gz`, `bz2`, `lz4`, `zst`, `lzma`, `xz` supported by [decompress](library/decompress.py) module. It can recognize file format only by extension, no content scan will be performed

Sometimes `uri` couldn't contain extension or even reliable filename. In this case you may set it by hand in `down_name` key. Temporary download will be placed to file in temporary directory with this name. Thus, decompress module able to handle file by extension

#### Single compressed download through controller

Case `1.2.2`:

```yaml
- url: "http://url.to/download.ext.gz"
  creates: "filename.ext"
  delegate_to: "localhost"
  archive: true
  files:
    - name: "filename.ext"
      dest: "/dir/on/target/host/with/"
```

Same stuff with decompress, but like `1.1.2` there will be performed a single download to Ansible controller. Either after successful download or updated `url` Ansible controller will decompress it to name from `creates` parameter. Then `ansible.builtin.copy` will spread file to destination hosts as the single element from `files:` list

#### Archive with a directory tree download to remote

Case `1.3.1`:

```yaml
- url: "http://url.to/download.tar.gz"
  creates: "filename.ext"
  dest: "/dir/on/target/host"
  archive: true
```

This will download a file to a remote host, perform `ansible.builtin.unarchive` and then traverse directory result directory with `chmod` directories to `dir_mode`, files with executive bit to `exec_mode` and non-executive files to `file_mode`

#### Archive with a directory tree download through controller

Case `1.3.2`:

```yaml
- url: "http://url.to/download.tar.gz"
  creates: "filename.ext"
  delegate_to: localhost
  dest: "/dir/on/target/host"
  archive: true
  files:
    - name: "relative/dir/of/file-in-archive.ext"
      dest: "sub-dir/from/parent/dest"
    - name: "some/other/in-archive.dump"
      dest: "/dir/for/other/"
    - name: "one/more/file-in-archive.jpg"
      dest: "/one/more/dir/picture.jpg"
```

There are a lot of options to upload by `files:` (shown as `f.` below) the full list:

- Both `dest` and `f.dest` are either relative or undefined or empty will raise error
- If `dest` is defined, it should be absolute otherwise error will be raised. Other options are similar as above:
  - Here `f.dest` can be empty or undefined, so `result = i.dest ~ '/' ~ f.name` w/o `basename`
  - If `f.dest` ended by `/`, `result = i.dest ~ '/' ~ f.dest ~ '/' ~ f.name | basename`
  - If `f.dest` is not ended by `/` then treated as file name: `result = i.dest ~ '/' ~ f.dest`
- If `dest` is empty the result should be defined by `f.dest` and `f.name`:
  - If `f.dest` finished by `/`, `result = f.dest ~ '/' ~ f.name | basename`
  - If `f.dest` is not finished by `/` then treated as path with filename: `result = f.dest`

Parameter `f.name` can be directory and will be recursively propagated. In this case two options of `f.name` are available to upload: w/ and w/o trailing `/`. Other rules are same as above multiplied on these options:

- If `f.name` ended by `/` only content of directory will be uploaded to the result
- Else the whole directory with content will be uploaded

This is the `ansible.builtin.copy` behavior. In both cases destination directory will be automatically created despite the result ended with `/` or not

## Role development road-map

### Replace `docker` to `podman` driver in molecule

Failed yet. I'm not able to start `systemd` inside a `podman in podman` container according to [article](https://www.redhat.com/en/blog/podman-inside-container). Grok and ChatGPT help also didn't work. However, `docker in podman` is tolerable here

Docker in docker also works. I choose the podman as first layer for the rootless approach which is impossible with the docker as a first layer. Probably, `podman --remote` with `--url` to host socket in podman should work. But there are no support for this in `molecule_podman` driver
