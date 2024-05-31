from flask import request, jsonify, render_template, redirect, url_for, current_app
from app.models import User
from app import db_session

@current_app.route('/')
def home():
    return render_template('index.html')

@current_app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        if not data or not all(k in data for k in ('name', 'surname', 'email', 'password')):
            return jsonify({'message': 'Missing required parameters'}), 400

        name = data['name']
        surname = data['surname']
        email = data['email']
        password = data['password']
        
        # Check if user already exists
        existing_user = db_session.query(User).filter_by(email=email).first()
        if existing_user:
            return jsonify({'message': 'User already exists'}), 400
        
        # Create new user
        new_user = User(name=name, surname=surname, email=email, password=password)
        db_session.add(new_user)
        db_session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    return render_template('register.html')

@current_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        if not data or not all(k in data for k in ('email', 'password')):
            return jsonify({'message': 'Missing required parameters'}), 400
        
        email = data['email']
        password = data['password']
        
        # Check if user exists and password is correct
        user = db_session.query(User).filter_by(email=email).first()
        if user and user.password == password:
            return jsonify({'message': f'Welcome, {user.name}!'}), 200
        return jsonify({'message': 'Invalid credentials'}), 401
    return render_template('login.html')

