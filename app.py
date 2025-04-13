from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from model import db, User, Service, Order, Review
from forms import RegisterForm, LoginForm,ReviewForm

import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'your-secret-key'



db.init_app(app)


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    services = Service.query.all()
    return render_template('home.html', services=services)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    services = Service.query.all()
    return render_template('services.html', services=services)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            role=form.role.data,
            name=form.name.data,
            email=form.email.data,
            mobile=form.mobile.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)  # Pass 'form' to template


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session['role'] == 'organizer':
        return render_template('dashboard_organizer.html')
    else:
        return render_template('dashboard_customer.html')

@app.route('/add_service', methods=['GET', 'POST'])
def add_service():
    if 'user_id' not in session or session['role'] != 'organizer':
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        description = request.form['description']
        price = request.form['price']
        image = request.files['image']

        image_filename = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_filename = filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_service = Service(
            title=title,
            category=category,
            description=description,
            price=price,
            image=image_filename,
            organizer_id=session['user_id']
        )
        db.session.add(new_service)
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('add_service.html')

@app.route('/service/<int:service_id>/review', methods=['GET', 'POST'])
def review(service_id):
    if 'user_id' not in session or session['role'] != 'customer':
        return redirect(url_for('login'))

    service = Service.query.get_or_404(service_id)
    form = ReviewForm()

    if form.validate_on_submit():
        review = Review(
            service_id=service.id,
            customer_id=session['user_id'],
            rating=int(form.rating.data),
            comment=form.comment.data
        )
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('services'))

    reviews = Review.query.filter_by(service_id=service_id).all()
    return render_template('review_form.html', form=form, service=service, reviews=reviews)

@app.route('/place_order/<int:service_id>', methods=['POST'])
def place_order(service_id):
    if 'user_id' not in session or session['role'] != 'customer':
        return redirect(url_for('login'))

    new_order = Order(service_id=service_id, customer_id=session['user_id'], status='Pending')
    db.session.add(new_order)
    db.session.commit()
    return redirect(url_for('profile_customer'))


@app.route('/profile/customer')
def profile_customer():
    if 'user_id' not in session or session['role'] != 'customer':
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    orders = Order.query.filter_by(customer_id=user.id).all()
    return render_template('profile_customer.html', user=user, orders=orders)

@app.route('/profile/organizer')
def profile_organizer():
    if 'user_id' not in session or session['role'] != 'organizer':
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])

    services = Service.query.filter_by(organizer_id=user.id).all()
    service_ids = [s.id for s in services]
    orders = Order.query.filter(Order.service_id.in_(service_ids)).all()

    return render_template('profile_organizer.html', user=user, services=services, orders=orders)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
