# Ansible actions from inventory variables

[![molecule](https://github.com/raven428/ansible-mega-var/actions/workflows/molecule.yaml/badge.svg)](https://github.com/raven428/ansible-mega-var/actions/workflows/molecule.yaml)

## Example usage from `site.yaml`

```yaml
- name: Perform some files, dirs, and templates upload
  hosts: mega_var
  become: true
  handlers:
    - import_tasks: handlers/main.yaml
  roles:
    - role: external/mega-var
      vars:
        meva_groups2create: "{{ meva_site_groups2create }}"
        meva_users2create: "{{ meva_site_users2create }}"
        meva_dirs2create: "{{ meva_site_dirs2create }}"
        meva_ghr2down: "{{ meva_site_ghr2down }}"
        meva_templates2upload: "{{ meva_site_templates2upload }}"
        meva_content2upload: "{{ meva_site_content2upload }}"
        meva_key2user: "{{ meva_site_key2user }}"
        meva_file2down: "{{ meva_site_file2down }}"
        meva_tree2rsync: "{{ meva_site_tree2rsync }}"
        meva_files2upload: "{{ meva_site_files2upload }}"
        meva_systemd4units: "{{ meva_site_systemd4units }}"
        meva_partitions: "{{ meva_site_partitions }}"
        meva_lvg: "{{ meva_site_lvg }}"
        meva_lvol: "{{ meva_site_lvol }}"
        meva_filesystems: "{{ meva_site_filesystems }}"
        meva_mounts: "{{ meva_site_mounts }}"
  tags: [mega-var]
```

## Role development road-map

- ✔ split into multiple files to allow usage of every single part from other roles with the tasks_from parameter
- ✔ role needs to be tested as one of the units in CI, e.g., by molecule:
  - ✔ calling the whole role
  - ✔ calling every of split tasks
  - ✔ check mode also should be tested because of a lot of check_mode: yes
- ❌ add to `c` plain HTTPS with basic and token auth options
- ✔ join `file2down` with `ghr2down` for the ability to download and unpack
- ✔ reduce verbosity of `get releases list` task by python module
- add all compressors tests for decompress module
- replace `docker` to rootless `podman` with [upgrade](https://github.com/raven428/container-images/blob/master/podman.sh) to recent version
