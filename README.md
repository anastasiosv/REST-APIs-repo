# Mock e-store Rest API

Mock e-store REST API is a Python REST API with Flask library and SQLAlchmeny which simulates an e-store.

# Running the REST API on Google Compute Engine instance

Creating a [Compute Engine instance](https://cloud.google.com/compute/docs/instances/create-start-instance):
```
gcloud beta compute --project=[project-name] instances create [instance-name] --zone=us-central1-a  --machine-type=n1-standard-1 --subnet=default --image=ubuntu-1604-xenial-v20200429 --image-project=ubuntu-os-cloud --boot-disk-size=10GB --boot-disk-type=pd-standard --boot-disk-device-name=instance-1
```

Adding root user password after sshing into the instance
```
sudo passwd
```

Log in as root user
```
apt-get update
apt-get install postgresql postgresql-contrib -y
```
Optionally you can check if postgresql is working as expected:
```
sudo -i -u postgres
psql
\conninfo to get some connection info
\q
exit
```
Adding new user/new group with the name [my-name]
```
adduser [my-name]
visudo to give creds to [my-name] user
```
Under this line: 
```
# User privilege specification"
root 	  ALL=(ALL:ALL) ALL
```
We have to add:
```
[my-name] ALL=(ALL:ALL) ALL

```
We execute the command:
```
vi /etc/ssh/sshd_config
```
At the end of the file add:
```
AllowUsers [my-name] 
```
Reload the service in order changes to take place.
```
service sshd reload
exit 
```

Connect now using your user and let's link user to postgresql
```
sudo su
sudo -i -u postgres
createuser [my-name] -P
createdb [my-name]
exit
exit
```
Now they are linked and I can run "psql" command from my terminal using my user

```
sudo vi /etc/postgresql/9.5/main/pg_hda.conf
```

At the end of the file I will make my postgresql more secure in order to avoid issues with SQLAlchemy changing:
local all all [peer] to
local all all [md5] 

I will proceed now to install the needed services and made some configurations:

```
sudo apt-get update 
sudo apt-get install nginx -y
sudo ufw status 
sudo ufw enable
sudo ufw allow 'Nginx HTTP'
sudo ufw allow ssh
systemctl status nginx
```
I am creating now the file item-rest.conf 
```
sudo vi /etc/nginx/sites-available/item-rest.conf
```
I will add inside that file the following script:

```
server {
	listen 80;
	real_ip_header X-Forwarded-For;
	set_real_ip_from 127.0.0.1;
	server_name localhost;

location / {
	include uwsgi_params;
	uwsgi_pass unix: /var/www/html/items-rest/socket.sock;
	uwsgi_modifier1 30;
}
error_page 404 /404.html;
location = /404.html {
	root /usr/share/nginx/html;
}

error_page 500 502 503 504 /50x.html;
location = /50x.html {
	root /usr/share/nginx/html;
}
}
```
I have to create a link between the file I created and the /etc/nginx/sites-enabled/
```
sudo ln -s /etc/nginx/sites-available/items-rest.conf /etc/nginx/sites-enabled/
```
I will create now the directory where we will host our code.
```
sudo mkdir /var/www/html/items-rest
sudo chown [my-name]:[my-name] /var/html/items-rest
cd /var/www/html/items-rest
git clone https://github.com/tassosv/REST-APIs-repo.git .
```
If you don't create a log directory, you will not be able to see logs.
```
mkdir log
```

After that you will need to install some needed libraries and create a virtual environment
```
sudo apt-get install python-pip python3-dev libpq-dev
pip install virtualenv
virtualenv venv --python=python3
source venv/bin/activate
pip install -r requirements.txt
sudo apt-get install libpcre3 libpcre3-dev
pip install uwsgi -I --no-cache-dir
```
Apart from that we should create the uwsgi_items_rest.service file
```
source vi /etc/systemd/system/uwsgi_items_rest.service
```
And write inside the file the following script:
```
[Unit]
Description=uWSGI items rest

[Service]
Environment=DATABASE_URL=postgres://[my-name]:[db-password]@localhost:5432/[my-name]
ExecStart=/var/www/html/items-rest/venv/bin/uwsgi --master --emperor /var/www/html/items-rest/uwsgi.ini --die-on-term --uid [my-name] --gid [my-name] --logto /var/www/html/items-rest/log/emperor.log
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```
Finally, you should update the uwsgi.ini
```
sudo vi uwsgi.ini
```
and update the file with the following script:
```
[uwsgi]
base = /var/www/html/items-rest
app  = run
module = %(app)

home = %(base)/venv
pythonpath = %(base)
socket = %(base)/socket.sock
chmod-socket = 777
processes = 8
threads = 8
harakiri = 15
callable = app
logto = /var/www/html/items-rest/log/%n.log
```

## How to run the app
```
sudo systemctl start uwsgi_items_rest 
```
You can check for the successful run of your REST API checking the logs
```
vi log/uwsgi.log
```
Basic steps before the final check:
```
sudo rm /etc/nginx/sites-enabled/default
```
You have to remove the default, otherwise you request you will end up on 404 error, and after all we will reload the nginx and we will start our service.

```
sudo systemctl reload nginx 
sudo systemctl restart nginx
sudo systemctl start uwsgi_items_rest
```

## Test Environemnt
Testing phase of our REST API took place on Postman Application. 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
