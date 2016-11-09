#flask modle generator

usage:
    1. define your db scheme in http://ondras.zarovi.cz/sql/demo/?keyword=default
    2. save scheme to db.xml file
    3. python fm_generaot.py db.xml


example:

INPUT:
``` sql
CREATE TABLE `user` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `user_name` VARCHAR(80) NULL DEFAULT NULL,
  `email` VARCHAR(120) NULL DEFAULT NULL,
   PRIMARY KEY (`id`, `user_name`, `email`)
);
```

OUTPUT:
``` python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        pass
```
