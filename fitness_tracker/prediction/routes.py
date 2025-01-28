from prediction import app
from prediction import db
from prediction.models import User
from .forms import HealthDataForm,SignupForm,LoginForm
from flask import render_template, redirect, url_for,flash,request,session
from flask_login import login_user,logout_user,login_required,current_user
import pandas as pd
import joblib
from datetime import date


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user_to_create = User(user_id = form.user_id.data,username = form.username.data,email_address = form.email.data,password = form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()

        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:
        for msg in form.errors.values():
            flash(f'Erorr Ocurred {msg}',category='danger')

    return render_template('signup.html',form = form)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username = form.username.data).first()
        attempted_password = User.query.filter_by(password_hash =form.password.data).first()
        if attempted_user and attempted_password:
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')
    return render_template('login.html',form=form)


@app.route('/predict',methods=['GET','POST'])
@login_required
def predict():
    form = HealthDataForm()
    if form.validate_on_submit():
        input_data = {
            'day_of_week': form.dayofweek.data,
            'steps_per_calorie': form.steps.data/form.calorie.data,
            'distance_km':form.distance.data,
            'active_minutes': form.active.data,
            'sleep_hours': form.sleep.data,
            'heart_rate_avg': form.heart.data,
            'workout_type': form.work_out_type.data,
            'weather_conditions': form.weather.data,
            'location': form.location.data
        }

        x = pd.DataFrame([input_data])
        try:
            user_model = loaded_user_models = joblib.load(r'D:\project\fitness_tracker\prediction\user_models.joblib')
        
        except Exception:
            print("Error occured")
        
        day_of_week_mapping = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
        x['day_of_week'] = x['day_of_week'].map(day_of_week_mapping)
        workout_type_mapping = {'Cycling': 0,'Walking': 1,'Running': 2,'Gym Workout': 3,'Yoga': 4,'Swimming': 5}
        x['workout_type'] = x['workout_type'].map(workout_type_mapping)
        location_mapping = {
        'Gym': 0,        # Highest count
        'Home': 1,
        'Office': 2,
        'Other': 3,
        'Park': 4 }
        x['location'] = x['location'].map(location_mapping)
        weather_conditions_mapping = {
        'Clear': 0,    # Highest count
        'Fog': 1,
        'Rain': 2,
        'Snow': 3}
        x['weather_conditions'] = x['weather_conditions'].map(weather_conditions_mapping)
        
        prediction = user_model[form.user_id.data].predict(x)
        session['prediction'] = prediction[0]
        session['input_data'] = input_data
        return redirect(url_for('display_prediction'))

    return render_template('form.html',form=form)

@app.route('/display')
def display_prediction():
    prediction = session.get('prediction')
    input_data = session.get('input_data')
    today = date.today()
    
    if prediction is None or input_data is None:
        flash('No prediction data available. Please submit the form first.', 'error')
        return redirect(url_for('health_data_form'))
    
    return render_template('display.html', prediction=prediction, input_data=input_data,today = today)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route('/api/users')
def users():
    users = User.query.all()
    return render_template('users.html',users=users)
    

