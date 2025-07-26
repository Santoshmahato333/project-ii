from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            flash('Please check your login details and try again.', 'error')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember)
        flash('Logged in successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('auth.signup'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('auth.signup'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return redirect(url_for('auth.signup'))
        
        # Check if user already exists
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('Username already exists.', 'error')
            return redirect(url_for('auth.signup'))
        
        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            flash('Email already registered.', 'error')
            return redirect(url_for('auth.signup'))
        
        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('auth.signup'))
    
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home')) 