from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Item
from sqlalchemy.exc import SQLAlchemyError
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a real secret key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db)

# Function to recreate the database
def recreate_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database tables dropped and recreated!")


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_tables():
    with app.app_context():
        db.create_all()

create_tables()

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('inventory'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('inventory'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        
        # Updated to use a valid hash method
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('inventory'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('inventory'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/inventory')
@login_required
def inventory():
    category = request.args.get('category')
    search = request.args.get('search')
    
    query = Item.query.filter_by(user_id=current_user.id)
    
    if category:
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(Item.name.ilike(f"%{search}%"))
    
    items = query.all()
    
    return render_template('inventory.html', items=items, category=category)

@app.route('/add_item', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        quantity = request.form.get('quantity')
        category = request.form.get('category')
        
        if not name or not quantity:
            flash('Name and quantity are required!', 'danger')
            return redirect(url_for('add_item'))
        
        try:
            quantity = int(quantity)
            if quantity < 0:
                raise ValueError
        except ValueError:
            flash('Quantity must be a positive integer!', 'danger')
            return redirect(url_for('add_item'))
        
        try:
            new_item = Item(name=name, description=description, quantity=quantity, category=category, user_id=current_user.id)
            db.session.add(new_item)
            db.session.commit()
            flash('Item added successfully!', 'success')
        except SQLAlchemyError:
            db.session.rollback()
            flash('Error while adding item. Try again.', 'danger')
        
        return redirect(url_for('inventory'))
    
    return render_template('add_item.html')

@app.route('/update_item/<int:id>', methods=['GET', 'POST'])
@login_required
def update_item(id):
    item = Item.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    if request.method == 'POST':
        item.name = request.form.get('name')
        item.description = request.form.get('description')
        item.quantity = request.form.get('quantity')
        item.category = request.form.get('category')
        
        try:
            db.session.commit()
            flash('Item updated successfully!', 'success')
        except SQLAlchemyError:
            db.session.rollback()
            flash('Error while updating item. Try again.', 'danger')
        
        return redirect(url_for('inventory'))
    
    return render_template('update_item.html', item=item)

@app.route('/delete_item/<int:id>')
@login_required
def delete_item(id):
    item = Item.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    try:
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted successfully!', 'success')
    except SQLAlchemyError:
        db.session.rollback()
        flash('Error while deleting item. Try again.', 'danger')
    
    return redirect(url_for('inventory'))

# Optional: Add a route for inventory visualization (data visualization)
@app.route('/inventory_visualization')
@login_required
def inventory_visualization():
    items = Item.query.filter_by(user_id=current_user.id).all()
    
    # Assuming categories and quantities are needed for visualization
    categories = {}
    for item in items:
        categories[item.category] = categories.get(item.category, 0) + item.quantity
    
    # This part would be for the frontend rendering using a JavaScript charting library like Chart.js
    return render_template('inventory_visualization.html', categories=categories)

if __name__ == '__main__':
    recreate_database()  # Call this function to recreate the database
    app.run(debug=True)

