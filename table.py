from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

hostname = 'localhost'
database = 'retreat'
username = 'postgres'
pwd = '123'
port_id = 5432

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{pwd}@{hostname}:{port_id}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Retreat(db.Model):
    __tablename__ = 'retreats'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.BigInteger, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(255), nullable=False)
    condition = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    tag = db.Column(db.ARRAY(db.String), nullable=False)
    duration = db.Column(db.Integer, nullable=False)


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), nullable=False)
    user_name = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(255), nullable=False)
    user_phone = db.Column(db.String(255), nullable=False)
    retreat_id = db.Column(db.Integer, db.ForeignKey('retreats.id'), nullable=False)
    retreat_title = db.Column(db.String(255), nullable=False)
    retreat_location = db.Column(db.String(255), nullable=False)
    retreat_price = db.Column(db.Float, nullable=False)
    retreat_duration = db.Column(db.Integer, nullable=False)
    payment_details = db.Column(db.String(255), nullable=False)
    booking_date = db.Column(db.BigInteger, nullable=False)

def insert_data():
    response = requests.get("https://669f704cb132e2c136fdd9a0.mockapi.io/api/v1/retreats")
    data = response.json()

    for item in data:
        retreat = Retreat(
            id=int(item["id"]),
            title=item["title"],
            description=item["description"],
            date=int(item["date"]),
            location=item["location"],
            price=float(item["price"]),
            type=item["type"],
            condition=item["condition"],
            image=item["image"],
            tag=item["tag"],
            duration=int(item["duration"])
        )
        db.session.add(retreat)

    db.session.commit()
    print("Data inserted successfully!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        insert_data()
        print("Tables created and data inserted successfully!")
