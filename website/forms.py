from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, length, NumberRange
from flask_wtf.file import FileField, FileRequired


class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), length(min=2)])
    password1 = PasswordField('Enter Your Password', validators=[DataRequired(), length(min=6)])
    password2 = PasswordField('Confirm Your Password', validators=[DataRequired(), length(min=6)])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Enter Your Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), length(min=6)])
    new_password = PasswordField('New Password', validators=[DataRequired(), length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), length(min=6)])
    change_password = SubmitField('Change Password')


class OrderForm(FlaskForm):
    customer_name = StringField('Customer Name', validators=[DataRequired()])
    customer_email = EmailField('Customer Email', validators=[DataRequired()])
    order_total = FloatField('Order Total', validators=[DataRequired()])
    submit = SubmitField('Place Order')


class ShopItemsForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    current_price = FloatField('Current Price', validators=[DataRequired()])
    previous_price = FloatField('Previous Price')
    in_stock = IntegerField('In Stock', validators=[DataRequired()])
    flash_sale = BooleanField('Flash Sale')
    product_picture = FileField('Product Picture')
    submit = SubmitField('Add Item')

    def __init__(self, *args, **kwargs):
        super(ShopItemsForm, self).__init__(*args, **kwargs)
        self.exclude = ['id']  # exclude the id field from validation