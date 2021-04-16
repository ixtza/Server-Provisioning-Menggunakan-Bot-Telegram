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
- hosts: localhost
  become_user: root
  tasks:
          - name: "stop mysql"
            service:
                    name: mysql
                    state: stopped
            become: true
```
pada bagian stop mysql secara keseluruhan hampir sama dengan start mysql bedanya hanya di statenya. untuk start mysql statenya adalah started dan untuk stop statenya adalah stopped dimana fungsi dari state stopped adalah memberhentikan proses mysql.

**Start Nginx**
```
- hosts: localhost
  become_user: root
  tasks:
          - name: "start nginx"
            service:
                    name: nginx
                    state: started
            become: true
```
pada bagian start nginx host yang digunakan adalah localhost dengan user root. service yang digunakan nginx dan statenya adalah started yang mengaktifkan proses nginx. sama seperti mysql, untuk mengatasi adanya permasalahan tanya password secara berulang maka digunakan become: true.

**Stop Nginx**
```

```
