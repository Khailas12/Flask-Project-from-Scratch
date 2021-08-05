from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)
    # lazy = Lazy parameter determines how the related objects get loaded when querying through relationships
    
    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'${str(self.budget)[:-3]},{str(self.budget)[-3:]}'

        else:
            return f'${self.budget}'
    
    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)      
    
    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

    def can_sell(self, item_obj):
        return item_obj in self.items
    
    
class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024),
                            nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
        
    def __repr__(self):
        return f'Item {self.name}'


    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()
        
    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()
        
    
# __repr__ is used to compute the “official” string representation of an object and is typically used for debugging


# ForeginKey = First you need to supply a primary key for each Model. Then you need to define one foreign key which refers to the Primary Key of the other model. Now you can define a relationship with a backref that allows direct access to the related model.


# acrssing db

# terminal > Python >
# from market.models import db
# db.drop_all()
# db.create_all()
# from market.models import User, Item
# u1 = User(username='jsc', password_hash='12345', email_address ='jsc@gmail.com')
# db.session.add(u1)
# db.session.commit()
# User.query.all()   -> Case sesnsitive

# >>> i1 = Item(name='IPhone 10', description='description', barcode='123456789123', price=800)
# db.session.addd(i1)
# db.session.commit()



