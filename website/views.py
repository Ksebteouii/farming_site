from flask import Blueprint, render_template
from flask_login import current_user

from website.models import Product

views = Blueprint('views', __name__)


@views.route('/')
def home():

    items = Product.query.filter_by(flash_sale=True)

    return render_template('home.html',items=items,current_user=current_user)