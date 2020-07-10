# Mini Wallet
&nbsp;
### How to setup and run server

#### 1. Virtual environment setup (Python version 3.6.9)
```sh
$ virtualenv -p python3 env
```
#### 2. Install requirements
```sh
$ source env/bin/activate
(env)$ pip install -r requirements.txt
```
#### 3. Migrate database
```sh
(env)$ Python manage.py migrate
```

#### 4. Run server (localhost)
```sh
(env)$ Python manage.py runserver
```