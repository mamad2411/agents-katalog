---
name: sky-ansible
description: >-
  Ansible ile sunucu yapılandırma otomasyonu: envanter, playbook ve roller, idempotent görevler,
  değişkenler ve şablonlar (Jinja2), handler'lar, Ansible Vault ile sırlar, sık kullanılan
  modüller (apt, user, copy, template, systemd, ufw, docker), check ve diff modu ile güvenli
  çalıştırma, Galaxy rolleri, Molecule ile test ve Terraform ile birlikte kullanım. Birden çok
  sunucuyu tekrarlanabilir şekilde kurmak/yapılandırmak gerektiğinde kullan.
disable-model-invocation: true
---

# Sky · Ansible

## Ne zaman?

Birden çok VPS'i aynı şekilde kurmak, sunucu yapılandırmasını kodla tutmak, tek sunucuyu bile felaketten sonra dakikalar içinde yeniden kurmak.
Altyapı oluşturma (sunucu, DNS, ağ) → Terraform (bkz. `sky-iac`); oluşan sunucunun **içini** yapılandırma → Ansible. Konteyner platformunda (K8s) çoğu zaman gerekmez.

## Yapı

```
ansible/
  inventory/prod.ini        # [web] 1.2.3.4 ansible_user=deploy
  group_vars/all.yml
  group_vars/all/vault.yml  # ansible-vault ile şifreli
  roles/
    base/      tasks/main.yml, handlers/main.yml, templates/
    caddy/
    app/
  site.yml
```

## Playbook

```yaml
# roles/base/tasks/main.yml
- name: Paketleri güncelle
  ansible.builtin.apt: { update_cache: true, upgrade: safe }
- name: Gerekli paketler
  ansible.builtin.apt: { name: [ufw, fail2ban, unattended-upgrades], state: present }
- name: SSH parola girişini kapat
  ansible.builtin.copy:
    dest: /etc/ssh/sshd_config.d/hardening.conf
    content: "PermitRootLogin no\nPasswordAuthentication no\n"
    mode: "0644"
  notify: SSH yeniden yükle
- name: Güvenlik duvarı kuralları
  community.general.ufw: { rule: allow, port: "{{ item }}", proto: tcp }
  loop: ["22", "80", "443"]
- name: Güvenlik duvarını etkinleştir
  community.general.ufw: { state: enabled, policy: deny }
```
```yaml
# roles/base/handlers/main.yml
- name: SSH yeniden yükle
  ansible.builtin.systemd: { name: ssh, state: reloaded }
```
- **Idempotent**: modüller "istenen durum"u tanımlar; ikinci çalıştırmada değişiklik olmamalı. `shell`/`command` son çare (gerekiyorsa `creates:` / `changed_when:`).
- Şablonlar `template:` + Jinja2 (`{{ app_domain }}`), değişkenler `group_vars`/`host_vars`.

## Sırlar

`ansible-vault encrypt group_vars/all/vault.yml`; parola dosyası Git'te değil (`--vault-password-file` veya parola yöneticisi betiği); vault değişkenlerini `vault_` önekiyle, normal değişkenlerden referansla.

## Güvenli çalıştırma

```bash
ansible-playbook -i inventory/prod.ini site.yml --check --diff     # önce kuru çalıştırma: ne değişecek?
ansible-playbook -i inventory/prod.ini site.yml --limit web1       # önce tek sunucu
```
SSH/güvenlik duvarı görevlerinde kendini kilitleme riski → önce staging'de dene, mevcut oturumu açık tut (bkz. `sky-linux-server`). `serial: 1` ile sunucuları sırayla güncelle (kesintisiz).

## Test ve paylaşım

`ansible-lint`, **Molecule** (Docker içinde rol testi), Ansible Galaxy rolleri (sürüm sabitleyerek, `requirements.yml`); CI'da lint + check modu.
