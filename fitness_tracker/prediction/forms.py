from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import IntegerField,FloatField,SelectField,StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired, NumberRange,Email,Length,EqualTo


class SignupForm(FlaskForm):
    user_id = IntegerField('User ID', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password1 = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class HealthDataForm(FlaskForm):
    user_id = IntegerField('User ID', validators=[DataRequired(), NumberRange(min=1)])
    dayofweek = SelectField('Day of the Week', 
                            choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
                                     ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'),
                                     ('Sunday', 'Sunday')],
                            validators=[DataRequired()])
    steps = FloatField('Number of Steps', validators=[DataRequired(), NumberRange(min=0)])
    calorie = FloatField('Calories Burned', validators=[DataRequired(), NumberRange(min=0)])
    distance = FloatField('Distance (km)', validators=[DataRequired(), NumberRange(min=0)])
    active = IntegerField('Active Minutes', validators=[DataRequired(), NumberRange(min=0)])
    sleep = FloatField('Sleep (hours)', validators=[DataRequired(), NumberRange(min=0, max=24)])
    heart = FloatField('Heart Rate', validators=[DataRequired(), NumberRange(min=0)])
    work_out_type = SelectField('Workout Type',choices=[('Cycling', 'Cycling'), ('Walking', 'Walking'), ('Running', 'Running'),
                                     ('Gym Workout', 'Gym Workout'), ('Yoga', 'Yoga'), ('Swimming', 'Swimming'),
                                     ], validators=[DataRequired()])
    weather = SelectField('Weather',choices=[('Clear', 'Clear'), ('Fog', 'Fog'), ('Rain', 'Rain'),
                                     ('Snow', 'Snow')
                                     ], validators=[DataRequired()])
    location = SelectField('Location',choices=[('Gym', 'Gym'), ('Home', 'Home'), ('Office', 'Office'),
                                     ('Other', 'Other'), ('Park', 'Park')
                                     ], validators=[DataRequired()])
    
