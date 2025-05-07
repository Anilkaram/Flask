from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, redirect

app = Flask(__name__)

# Configure PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:password@localhost:5432/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

# Create the database tables
@app._got_first_request
def create_tables():
    db.create_all()

# Route to add a user
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(name=data['name'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': f'User {new_user.name} added successfully'}), 201

# Route to list users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name} for user in users])

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        db.session.add(User(name=name))
        db.session.commit()
        return redirect('/')
    users = User.query.all()
    return render_template('index.html', users=users)