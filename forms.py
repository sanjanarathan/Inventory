from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange

# Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField('Register')

# Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Item Form for adding/updating items
class ItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()])
    description = StringField('Description')
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    category = StringField('Category')
    submit = SubmitField('Submit')
