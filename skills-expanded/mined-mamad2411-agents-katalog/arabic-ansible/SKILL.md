---
name: arabic-ansible
name_ar: أنسيبل
description: Master automation with Ansible in Arabic
description_ar: إتقان الأتمتة مع أنسيبل بالعربية
category: developer
language: ar
dialect: msa
rtl: true
platform_all: true
version: 1.0.0
author: salman-shaikh
---

## الهدف

إتقان أتمتة البنية التحتية والتطبيقات باستخدام Ansible.

## المفاهيم الأساسية

| المصطلح | الوصف |
|---------|-------|
| Inventory | قائمة السيرفرات |
| Playbook | مهام YAML |
| Task | مهمة واحدة |
| Module | وحدة تنفيذ |
| Role | حزمة مهام قابلة لإعادة الاستخدام |
| Handler | مهمة تعمل عند التغيير |

## تثبيت Ansible

```bash
# Ubuntu
sudo apt install ansible

# pip
pip install ansible

# التحقق
ansible --version
```

## Inventory ملف

```ini
# hosts
[webservers]
web1.example.com
web2.example.com

[dbservers]
db1.example.com ansible_ssh_user=root

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

## Playbook مثال

```yaml
# deploy.yml
---
- name: Deploy Web Server
  hosts: webservers
  become: yes
  vars:
    http_port: 80
    max_clients: 200
  
  tasks:
    - name: Install Apache
      apt:
        name: apache2
        state: present
      notify: restart apache
    
    - name: Start Apache
      service:
        name: apache2
        state: started
        enabled: yes
    
    - name: Configure firewall
      ufw:
        rule: allow
        port: "{{ http_port }}"
        proto: tcp
    
    - name: Deploy website
      copy:
        src: /var/www/html
        dest: /var/www/
        owner: www-data
        group: www-data
        mode: '0644'
  
  handlers:
    - name: restart apache
      service:
        name: apache2
        state: restarted
```

## Modules شائعة

```yaml
# إدارة حزم
- apt:
    name: nginx
    state: present

# إدارة ملفات
- copy:
    src: file.txt
    dest: /tmp/

- template:
    src: config.j2
    dest: /etc/app/config.yml

# إدارة خدمات
- service:
    name: nginx
    state: restarted

# إدارة مستخدمين
- user:
    name: ahmed
    state: present
    groups: sudo

# تنفيذ أوامر
- command: ls -la
  register: output

- debug:
    var: output
```

## Roles هيكل

```
roles/
├── webserver/
│   ├── tasks/
│   │   └── main.yml
│   ├── handlers/
│   │   └── main.yml
│   ├── templates/
│   ├── files/
│   ├── vars/
│   │   └── main.yml
│   └── defaults/
│       └── main.yml
```

## Templates (Jinja2)

```jinja2
# config.yml.j2
server:
  port: {{ http_port }}
  max_connections: {{ max_clients }}
  environment: {{ env_name }}

{% for server in servers %}
  - name: {{ server.name }}
    ip: {{ server.ip }}
{% endfor %}
```

## تشغيل Playbook

```bash
# تشغيل عادي
ansible-playbook deploy.yml

# مع inventory مخصص
ansible-playbook -i hosts.ini deploy.yml

# مع متغيرات
ansible-playbook deploy.yml -e "http_port=8080"

# محاكاة فقط (dry run)
ansible-playbook deploy.yml --check

# خطوة بخطوة
ansible-playbook deploy.yml --step

# استهداف مجموعة
ansible-playbook deploy.yml --limit webservers
```

## أفضل الممارسات

✅ استخدم roles لإعادة الاستخدام
✅ استخدم tags للمهام
✅ استخدم vault للأسرار
✅ اختبر في بيئة تطوير أولاً
✅ استخدم version control

❌ لا تستخدم become إلا للضرورة
❌ لا تخزن كلمات مرور في plain text
❌ لا تشغل على production بدون اختبار

---

## الكلمات المفتاحية

عربي: "أنسيبل", "أتمتة", "إعداد سيرفرات"
English: "ansible arabic", "automation", "configuration management"

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي
