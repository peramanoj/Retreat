from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_

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

@app.route('/retreats', methods=['GET'])
def get_retreats():
    search = request.args.get('search', '')
    location = request.args.get('location', '')
    tags = request.args.get('tags', '')
    type_ = request.args.get('type', '')
    page = request.args.get('page', type=int, default=1)
    limit = request.args.get('limit', type=int, default=10)

    query = db.session.query(Retreat)

    if search:
        search = f"%{search}%"
        query = query.filter(or_(
            Retreat.title.ilike(search),
            Retreat.location.ilike(search),
            Retreat.type.ilike(search),
            Retreat.condition.ilike(search),
            Retreat.description.ilike(search)
        ))
    if location:
        query = query.filter(Retreat.location.ilike(f"%{location}%"))
    if tags:
        tags_list = tags.split(',')
        query = query.filter(and_(*[Retreat.tag.any(tag) for tag in tags_list]))
    if type_:
        query = query.filter(Retreat.type.ilike(f"%{type_}%"))

    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    retreats = pagination.items

    retreats_list = [{
        'id': retreat.id,
        'title': retreat.title,
        'description': retreat.description,
        'date': retreat.date,
        'location': retreat.location,
        'price': retreat.price,
        'type': retreat.type,
        'condition': retreat.condition,
        'image': retreat.image,
        'tag': retreat.tag,
        'duration': retreat.duration
    } for retreat in retreats]

    return jsonify({
        'page': pagination.page,
        'pages': pagination.pages,
        'total': pagination.total,
        'per_page': pagination.per_page,
        'retreats': retreats_list
    })

@app.route('/book', methods=['POST'])
def create_booking():
    data = request.get_json()
    booking = Booking(
        user_id=data['user_id'],
        user_name=data['user_name'],
        user_email=data['user_email'],
        user_phone=data['user_phone'],
        retreat_id=data['retreat_id'],
        retreat_title=data['retreat_title'],
        retreat_location=data['retreat_location'],
        retreat_price=data['retreat_price'],
        retreat_duration=data['retreat_duration'],
        payment_details=data['payment_details'],
        booking_date=data['booking_date']
    )
    
    # Check if retreat is already booked by the user
    existing_booking = Booking.query.filter_by(user_id=data['user_id'], retreat_id=data['retreat_id']).first()
    if existing_booking:
        return jsonify({'error': 'This retreat is already booked by the user'}), 400
    
    db.session.add(booking)
    db.session.commit()
    
    return jsonify({'message': 'Booking created successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
