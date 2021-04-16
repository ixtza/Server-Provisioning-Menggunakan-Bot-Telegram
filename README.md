# Server-Provisioning-Menggunakan-Bot-Telegram

Penugasan camin periode 2021

## Tabel Konten

## Peringatan

- Modul dibuat berdasarkan tujuan non-praktis atau sebatas pengalaman.
- Diharapkan pembaca untuk tidak menjadikan modul ini sebagai acuan utama dalam melakukan otomasi _server provisioning_.
- Pembuat modul tidak bertanggung jawab bila terjadi kerusakan sistem akibat serangan dari luar atau kesalahan konfigurasi.

## Pengantar

_Provisioning_ merupakan proses pengaturan infrastruktur IT. Terdapat banyak jenis _provisioning_ dan salah satunya _server provisioning_.

_Server provisioning_ adalah proses pengaturan server agar digunakan sesuai kebutuhan. Kegiatan ini termaksud pengaturan perangkat keras di pusat data, instalasi, dan pengaturan perangkat lunak (sistem operasi, aplikasi, jaringan, penyimpanan, dan lainnya).

Kegiatan _server provisioning_ yang awalnya berbentuk proses dapat dipersingkat dengan adanya bantuan program otomasi seperti `Ansible` dengan bantuan `Telegram Bot` sebagai antarmukanya.

Pada modul ini, akan dibahas cara melakukan _server provisioning_ dari segi perangkat lunak menggunakan bantuan `Ansible`, webhook `Ngrok`, dan `Telegram Bot`.

## Ansible

Ansible adalah alat otomasi untuk penyediaan, penyebaran aplikasi, dan manajemen konfigurasi. Dengan meggunakan SSH untuk masuk ke server untuk menjalankan perintah atau mengakses bersama-sama dengan skrip bash/terminal untuk semi-otomatis mengotomatiskan _task_ yang sulit sekalipun.

### Menyiapkan SSH

`Ansible` memanfaatkan protokol SSH untuk berinteraksi antar mesin dengan server. Berikut tahapan menyiapkannya:

- Di bagian server instal _package_ `OpenSSH-Server` ke server.

```bash
sudo apt-get install openssh-server
```

- Restart dan cek apakah layanan SSH berjalan. (Jika berhasil akan ada status `Running` saat menjalankan perintah ke dua).

```bash
sudo systemctl start ssh
sudo systemctl status ssh
```

- Sekarang dibagian _client_ (bukan server) buat pasangan kunci(publik dan privat) enkripsi RSA.

```bash
ssh-keygen
```

- akan muncul hasil seperti berikut.

```
Generating public/private rsa key pair.
Enter file in which to save the key (/~/.ssh/id_rsa):
```

- Jika ingin menggunakan _default path_ silahkan langsung tekan `enter`, atau bisa menyediakan alternatif tempat lain.

```
/home/your_home/.ssh/id_rsa already exists.
Overwrite (y/n)?
```

- Jika sebelumnya sudah pernah membuat kunci enkripsi akan muncul notifkasi diatas. Sesuai kebutuhan, jika ingin menggantinya silahkan ketik `y` lalu `enter`. Atau ketik `n` lalu di langgkah pengaturan _path_ disesuaikan.

```
Enter passphrase (empty for no passphrase):
```

- Jika sudah, akan diminta untuk menambahkan otentikasi tambahan (opsional).

```
Your identification has been saved in /~/.ssh/id_rsa
Your public key has been saved in /~/.ssh/id_rsa.pub
The key fingerprint is:
...
```

- Jika berhasil akan muncul hasil seperti diatas. Bisa dilihat terdapat `id_rsa` dan `id_rsa.pub`, yang kita gunakan nanti adalah `id_rsa.pub`.
- Kemudian kita akan menaruh `id_rsa.pub` ke dalam server dengan perintah.

```bash
cat ~/.ssh/id_rsa.pub | ssh (username_server)@(remote_host/ip server) "mkdir -p ~/.ssh && touch ~/.ssh/authorized_keys && chmod -R go= ~/.ssh && cat >> ~/.ssh/authorized_keys"

```

- Nantinya, akan diminta **password server** untuk menjalankan perintah ini.

Sekarang kita dapat melakukan SSH ke server tanpa password. Hal yang selanjutnya kita lakukan adalah mengatur agar `username_server` dapat menjalankan perintah tanpa `sudo password`:

- Lakukan SSH ke server.

```
ssh (username_server)@(remote_host/ip server)
```

- Mengatur akses sudo dengan

```
sudo visudo
```

- nantinya akan muncul tampilan dan pada salah satu line terdapat.

```
...
%sudo ALL=ALL(ALL:ALL) ALL
...
```

- tambahkan `username_server` dibawah line tersebut.

```
...
%sudo ALL=ALL(ALL:ALL) ALL
[(`username_server`)] ALL=(ALL) NOPASSWD:ALL
...
```

- Kemudian `ctrl + s` lalu `ctrl + x` **, lalu keluar dari ssh server**.

### Menyiapkan Ansible

**Jika sudah kembali ke sistem _client_.** Saatnya kita mengatur `Ansible`. Juga, diharapkan sudah memasang **`Python`** versi 3 ke atas.

- Tambahkan _repository_ distribusi `Ansible` yang resmi.

```
sudo apt-add-repository ppa:ansible/ansible
```

- _Update_ _package_ sistem agar tau _repository_ yang baru kita tambahkan.

```
sudo apt update
```

- Instal _package_ Ansible.

```
sudo apt install ansible
```

- Atur konfigurasi jaringan `Ansible` di,

```
sudo nano /etc/ansible/hosts
```

- Akan muncul tampilan berikut

```
...
[servers]
server1 ansible_host=203.0.113.111
server2 ansible_host=203.0.113.112
.
.
(nama samaran server) ansible_host=(remote_host/ip server)

[all:vars]
ansible_python_interpreter=/usr/bin/python3
...
```

- Ganti `nama samaran server` sesuai keinginan dan `remote_host/ip server` ke ip server target yang ingin di _provisioning_.
- Uji, apakah konfigurasi berhasil dengan,

```
ansible all -m ping -u root
```

- akan didapathkan hasil seperti berikut,

```
server1 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
server2 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

- `pong` berarti sistem sudah mendapatkan _feedback_ dari server.

### Menyiapkan Playbook

Sesudah melakukan konfigurasi saatnya kita membuat script otomasi `playbook` guna dijalankan oleh `Ansible`.

- buat sebuah script dalam bentuk `json` atau `yml`. Modul ini membuat `playbook` dengan format `yml` dengan nama `nginx_stop.yml`.

```
sudo nano /etc/ansible/nginx_start.yml
```

- kemudian bisa di _copas_ [script ini](#start-nginx) ke dalam `nginx_stop.yml`.
- **Ganti `localhost` menjadi (nama samaran server) yang sebelumnya sudah kita atur.** Jika lupa gunakan perintah.

```
ansible-inventory --list -y
```

- Jika sudah, `ctrl + s` lalu `ctrl + x`.
- Bisa dicoba pilihan lainnya sesuai contoh yang ada.
- Untuk menuji apakah berhasil jalankan perintah

```
ansible-palybook /etc/ansible/nginx_stop.yml
```

- Jika tidak ada error atau kendala, maka `playbook` berhasil dijalankan.

## Contoh `YML` Playbook

**Start MySql**

```yml
---
- hosts: localhost
  become_user: root
  tasks:
    - name: "start nginx"
      service:
        name: mysql
        state: started
      become: true
```

pada bagian start mysql digunakan hosts localhost dan user root. service yang digunakan adalah mysql. untuk mengatasi permasalahan tanya password secara berulang digunakan `become:true`

**Stop MySql**

```yml
---
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

```yml
---
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

```yml
---
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

## Daftar Pustaka

- https://www.redhat.com/en/topics/automation/what-is-provisioning
- https://medium.com/@skinnyboys/setupansible-1db87a1c8c30
- https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-ansible-on-ubuntu-18-04
- https://www.cyberciti.biz/faq/ubuntu-linux-install-openssh-server/
