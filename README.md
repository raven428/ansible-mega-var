# Ansible actions from inventory variables

## Example usage from `site.yaml`

```yaml
- name: perform some files, dirs, and templates upload
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

## Molecule tests todo

### Releases for testing
- [public](https://github.com/raven428/finch-externaleditor/releases)
- [private](https://github.com/raven428/far-smartpad/releases)

### File types for downloading (c)
1. simple HTTPS connection by URI
2. release from GitHub for platform and version lookup w/o auth token
3. release from GitHub for platform and version lookup using auth token

### File type to unpack (p)
1. single raw
2. single compressed
3. archive with directory tree

### Transfer options (b)
1. directly to target host
2. at the Ansible controller with `copy:`
3. at the Ansible controller with `synchronize:`

### check_mode (m)
1. no
2. yes

total `3 * 3 * 3 * 2 = 54` downloading tests

### Update options (u)
Only for p2, with c1-c5, b1-b3 and m1-m2

additional `1 * 3 * 3 * 2 = 18` update tests

### Linters
--"--

## Role development road-map

### Add to `c`
1. plain HTTPS with basic auth
2. plain HTTPS with token auth

### Other improvements
- it should be split into multiple files to allow usage of every single part from other roles with the tasks_from parameter
- it needs to be tested as one of the units in CI, e.g., by molecule:
  - calling the whole role
  - calling every of split tasks
  - check mode also should be tested because the role contains a lot of check_mode: yes parameters
- elaborate Ansible module for getting the exact URL of the GitHub release file to avoid flooding the Ansible log
- join `file2down` with `ghr2down` for the ability to download and unpack
