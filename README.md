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
