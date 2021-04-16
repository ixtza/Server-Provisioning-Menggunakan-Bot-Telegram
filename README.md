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
- hosts: localhost
  become_user: root
  tasks:
          - name: "stop nginx"
            service:
                    name: nginx
                    state: stopped
            become: true
```
pada bagian stop nginx secara keseluruhan hampir sama dengan start nginx bedanya hanya di statenya. untuk start nginx statenya adalah started dan untuk stop statenya adalah stopped dimana fungsi dari state stopped adalah memberhentikan proses nginx.

# Buat telegram bot

Tambahkan akun botfather, lalu masukkan perintah /newbot lalu masukkan data-data yang diminta

![image](https://user-images.githubusercontent.com/11045113/115054946-0c9cee80-9f0b-11eb-8cd5-156a24c3722a.png)

Akan didapatkan API token, catat untuk langkah selanjutnya

# Buat script python untuk mengolah perintah

```python
import requests
import os
import boturl
from bottle import (
    run, post, response, request as bottle_request
)
```

import fungsi-fungsi yang dibutuhkan + file boturl yang berisi api token bot

```python
BOT_URL = boturl.BOT_URL
```

definisikan BOT_URL

```python
def get_chat_id(data):
    chat_id = data['message']['chat']['id']
    return chat_id
```

fungsi untuk mengambil chat_id dari data request json

```python
def get_message(data):  
    message_text = data['message']['text']
    return message_text
```

fungsi untuk mengambil message dari user

```python
def send_message(prepared_data):  
    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=prepared_data)
```

fungsi untuk mengirim message kembali ke bot telegram

```python
def prepare_data_for_answer(data):  
    answer = "done"

    json_data = {
        "chat_id": get_chat_id(data),
        "text": answer,
    }

    return json_data
```

menyiapkan data untuk dikirim, dengan membuat data json berisi chat_id agar pesan terkirim ke user yang benar dan string berisi "done"

```python
@post('/')
def main():  
    data = bottle_request.json  # <--- extract all request data
    query = get_message(data)
    answer_data = prepare_data_for_answer(data)
```

fungsi main untuk mengambil semua data dari json, memasukkan message ke variabel query, dan menyiapkan data untuk dikirim balik

```python
    if query == "tes":
        send_message(answer_data)
    elif query == "nginx start":
        os.system("cd ~/ansible && ansible-playbook -i inventory.yml nginx_start.yml")
        send_message(answer_data)
    elif query == "nginx stop":
        os.system("cd ~/ansible && ansible-playbook -i inventory.yml nginx_stop.yml")
        send_message(answer_data)
    elif query == "mysql start":
        os.system("cd ~/ansible && ansible-playbook -i inventory.yml mysql_start.yml")
        send_message(answer_data)
    elif query == "mysql stop":
        os.system("cd ~/ansible && ansible-playbook -i inventory.yml mysql_stop.yml")
        send_message(answer_data)
```

if else untuk mengecek query yang diterima, berisi query tes yang hanya mengirim balik pesan untuk mengecek koneksi, dan query-query yang memanggil perintah bash yang sesuai, lalu mengirim balik pesan

```python
return response
```

mengembalikan response ke terminal, jika sukses maka di terminal akan tertulis 200 setiap ada request

```python
if __name__ == '__main__':  
    run(host='localhost', port=8080, debug=True)
```

mendengarkan port 8080 jika script dijalankan

simpan script tersebut dengan nama bot.py

# Buat webhook dengan ngrok

1. Download ngrok di websitenya
2. Install python3 dan pip3
3. Install bottle requests dengan pip3

```
pip3 install bottle requests  
```

4. Jalankan ngrok dengan

```
./ngrok http 8080
```

5. Akan muncul jendela ngrok, lalu salin url httpsnya

![image](https://user-images.githubusercontent.com/11045113/115055467-a82e5f00-9f0b-11eb-9091-d8c7c1c7f8ac.png)

6. Gabungkan dengan API token yang sudah dibuat, lalu masukkan ke address bar browser favorit anda, lalu tekan enter

api. telegram. org/bot<api_token_anda>/setWebHook?url=https://<url_ngrok_anda.ngrok.io/

7. Jalankan script python tadi di terminal

```
python3 bot.py
```

8. Coba tambahkan jadi teman bot anda di telegram, tulis tes, lalu kirim, bot akan merespon

![image](https://user-images.githubusercontent.com/11045113/115056457-16275600-9f0d-11eb-865c-35d514ae6cb9.png)

9. Cek status nginx/ mysql anda dengan

```
systemctl status nginx
```

![image](https://user-images.githubusercontent.com/11045113/115056729-63a3c300-9f0d-11eb-9ecf-1939e6b5cca8.png)

10. Jika nyala tuliskan 'nginx stop', jika mati tuliskan 'nginx start', di bot telegram, lalu kirim

![image](https://user-images.githubusercontent.com/11045113/115056814-7a4a1a00-9f0d-11eb-9a12-3ed3a12cbea2.png)

11. Cek status lagi, maka akan terlihat perubahannya

![image](https://user-images.githubusercontent.com/11045113/115056877-8afa9000-9f0d-11eb-8a8f-319932d9cd6a.png)

# Referensi:

https://djangostars.com/blog/how-to-create-and-deploy-a-telegram-bot/
