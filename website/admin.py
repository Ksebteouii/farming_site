from flask import Blueprint, flash, redirect, render_template, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .forms import ShopItemsForm, OrderForm
from .models import Product, Order, Customer
from . import db
from flask import send_from_directory
import os

admin = Blueprint('admin', __name__)

@admin.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory('media', filename)


@admin.route('/add-shop-items', methods=['GET', 'POST'])
@login_required
def add_shop_items():
    print("Accessing /add-shop-items route")
    if current_user.id == 1:
        print("Current user is admin")
        form = ShopItemsForm()
        if form.validate_on_submit():
            print("Form validated successfully")
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data if form.previous_price.data else None
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data
            file = form.product_picture.data

            if file:
                try:
                    file_name = secure_filename(file.filename)
                    media_dir = os.path.join(current_app.root_path, 'edia')
                    if not os.path.exists(media_dir):
                        os.makedirs(media_dir)
                    file_path = os.path.join(media_dir, file_name)
                    print(f"Saving file to {file_path}")
                    file.save(file_path)
                    print(f"File {file_name} saved successfully")

                    new_shop_item = Product(
                        product_name=product_name,
                        current_price=current_price,
                        previous_price=previous_price,
                        in_stock=in_stock,
                        flash_sale=flash_sale,
                        product_picture=file_name
                    )

                    try:
                        db.session.add(new_shop_item)
                        db.session.commit()
                        print('Product added to database')
                        flash(f'{product_name} added successfully')
                        return redirect(url_for('admin.shop_items'))
                    except Exception as e:
                        print(f"Error adding product to database: {e}")
                        flash('Error adding product')
                        db.session.rollback()  # Rollback the session in case of error

                except Exception as e:
                    print(f"Exception occurred: {e}")
                    flash('Error uploading file')

            else:
                print("No file uploaded")
                flash('No file uploaded')

        else:
            print("Form validation failed")
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error in {field}: {error}")

        return render_template('add_shop_items.html', form=form)

    print("User is not admin, rendering 404")
    return render_template('404.html')

@admin.route('/shop-items', methods=['GET', 'POST'])
@login_required
def shop_items():
    if current_user.id == 1:
        items = Product.query.order_by(Product.date_added).all()
        return render_template('shop_items.html', items=items)
    return render_template('404.html')

@admin.route('/delete-shop-item/<int:item_id>', methods=['POST'])
@login_required
def delete_shop_item(item_id):
    if current_user.id == 1:
        try:
            item_to_delete = Product.query.get(item_id)
            db.session.delete(item_to_delete)
            db.session.commit()
            flash('One Item deleted')
            return redirect(url_for('admin.shop_items'))
        except Exception as e:
            print('Item not deleted', e)
            flash('Item not deleted!!')
        return redirect(url_for('admin.shop_items'))

    return render_template('404.html')

@admin.route('/update-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    if current_user.id == 1:
        item = Product.query.get_or_404(item_id)
        form = ShopItemsForm()

        if form.validate_on_submit():
            item.product_name = form.product_name.data
            item.current_price = form.current_price.data
            item.previous_price = form.previous_price.data
            item.in_stock = form.in_stock.data
            item.flash_sale = form.flash_sale.data

            file = form.product_picture.data

            if file:
                try:
                    file_name = secure_filename(file.filename)
                    media_dir = os.path.join(current_app.root_path, 'media')
                    if not os.path.exists(media_dir):
                        os.makedirs(media_dir)
                    file_path = os.path.join(media_dir, file_name)
                    file.save(file_path)
                    item.product_picture = file_name
                except Exception as e:
                    print(e)
                    flash('Error updating product picture')

            db.session.commit()
            flash(f'{item.product_name} updated successfully')
            return redirect(url_for('admin.shop_items'))

        form.product_name.data = item.product_name
        form.current_price.data = item.current_price
        form.previous_price.data = item.previous_price
        form.in_stock.data = item.in_stock
        form.flash_sale.data = item.flash_sale

        return render_template('update_item.html', form=form, item=item)
    return render_template('404.html')