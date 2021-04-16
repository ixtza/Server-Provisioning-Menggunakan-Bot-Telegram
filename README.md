# Server-Provisioning-Menggunakan-Bot-Telegram

Penugasan camin periode 2021

**Start MySql**
```
- hosts: localhost
  become_user: root
  tasks:
          - name: "start nginx"
            service:
                    name: mysql
                    state: started
            become: true
```
pada bagian start mysql digunakan hosts localhost dan user root. service yang digunakan adalah mysql. untuk mengatasi permasalahan tanya password secara berulang digunakan become:true

**Stop MySql**
```

```
