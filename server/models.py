from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

   
    signups = db.relationship("Signup", backref="activity")
    
    serialize_rules = ("-signups.activity",)

    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    
    signups = db.relationship("Signup", backref="camper")
   
    serialize_rules = ("-signups.camper",)
   
    @validates("name")
    def validate_name(self, db_column, name):
        if type(name) is str and len(name) > 0:
            return name
        else:
            raise ValueError("Name must be a string.")

    @validates("age")
    def validate_age(self, db_column, age):
        if  type(age) is int and 8 <= age <= 18:
            return age
        else:
            raise ValueError("Age must be between 8 and 18")


    
    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)

    
    camper_id = db.Column(db.Integer, db.ForeignKey("campers.id"))
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id"))
    
    serialize_rules = ("-camper.signups", "-activity.signups")
   
    @validates("time")
    def validate_time(self, db_column, time):
        if type(time) is int and 0 <= time <= 23:
            return time 
        else:
            raise ValueError("Time must be within 0 and 23 hours.")

    @validates("activity_id")
    def validate_activity_id(self, db_column, activity_id):
        activity = Activity.query.get(activity_id)
        if activity:
            return activity_id
        else:
            return Exception("Activity not found.")
    
    @validates("camper_id")
    def validate_camper_id(self, camper_id, db_column):
        camper = Camper.query.get(camper_id)
        if camper:
            return camper_id
        else:
            return Exception("Camper not found.")

    def __repr__(self):
        return f'<Signup {self.id}>'


# add any models you may need.



# 1: run pipenv install and pipenv shell
# 2: export FLASK_APP=server/app.py
# 3: flask db init, to initialze the db file
# 4: flask db upgrade head to upgrade to models
# 5: add all relationships. first add the foreign keys to the table connecting 
# the others, then add a relationship that connects the other two to the 
# connector letting it be a reference to the Sign model
# 6: after finishing relationships
    # flask db revision --autogenerate -m 'message'
    # flask db upgrade head
    # python server/seed.py
# 7: you can go into DEBUG FILE to see if it had worked and check backref
    # Camper.query.all()
    # camper1 = Camper.query.all()[0]
    # camper1
    # camper1.signups
    # su1 = camper1.signups[0]
    # su1.camper //  this will show if the relationship between camper and 
# signups is working
    # su1.activity.name to check activity
# 8: Must add validators in order to make sure we are adding according to rules 
# and not adding incorrect values
    # When adding validators for our connector we must add validators for our 
# foreign keys as well where they must equal the id from the model of that 
# 9: add serialization 
