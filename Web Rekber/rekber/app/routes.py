from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import emit, join_room, leave_room
from . import db, bcrypt, socketio
from .models import User, Transaction, ChatMessage
from datetime import datetime, timedelta

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('main.admin_dashboard'))
    return render_template('dashboard.html')

@bp.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('main.dashboard'))
    transactions = Transaction.query.all()
    return render_template('admin_dashboard.html', transactions=transactions)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            if user.is_admin:
                return redirect(url_for('main.admin_dashboard'))
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.admin_dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email, is_admin=True).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('main.admin_dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('admin_login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/chat/<int:transaction_id>')
@login_required
def chat(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    messages = ChatMessage.query.filter_by(transaction_id=transaction_id).order_by(ChatMessage.timestamp.asc()).all()
    return render_template('chat.html', transaction=transaction, messages=messages)

@bp.route('/open_ticket', methods=['GET', 'POST'])
@login_required
def open_ticket():
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        transaction_type = request.form.get('transaction_type')
        amount = float(request.form.get('amount'))
        buyer_username = request.form.get('buyer_username')
        fee = amount * 0.05  # Contoh perhitungan fee 5%
        
        transaction = Transaction(
            item_name=item_name,
            transaction_type=transaction_type,
            amount=amount,
            buyer_username=buyer_username,
            fee=fee,
            owner=current_user
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Tiket transaksi berhasil dibuka!', 'success')
        return redirect(url_for('main.chat', transaction_id=transaction.id))
    return render_template('open_ticket.html')

@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('message', {'msg': f'{current_user.username} has entered the room.'}, room=room)

@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    leave_room(room)
    emit('message', {'msg': f'{current_user.username} has left the room.'}, room=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    message = ChatMessage(
        transaction_id=data['transaction_id'],
        sender_id=current_user.id,
        message=data['msg']
    )
    db.session.add(message)
    db.session.commit()
    emit('message', {'msg': f'{current_user.username}: {data["msg"]}'}, room=room)

@socketio.on('deal')
def handle_deal(data):
    transaction = Transaction.query.get(data['transaction_id'])
    if current_user.username == transaction.owner.username:
        transaction.seller_agreement = True
    elif current_user.username == transaction.buyer_username:
        transaction.buyer_agreement = True

    db.session.commit()

    if transaction.seller_agreement and transaction.buyer_agreement:
        transaction.status = 'deal'
        db.session.commit()
        emit('message', {'msg': 'Transaksi telah disepakati oleh kedua belah pihak.'}, room=data['room'])
    else:
        emit('message', {'msg': f'{current_user.username} telah menyetujui transaksi.'}, room=data['room'])

@socketio.on('non_deal')
def handle_non_deal(data):
    transaction = Transaction.query.get(data['transaction_id'])
    transaction.status = 'non_deal'
    db.session.commit()
    emit('message', {'msg': 'Transaksi tidak disepakati.'}, room=data['room'])

    # Logika untuk pembatalan otomatis setelah 1 jam
    def cancel_transaction():
        if transaction.status == 'pending':
            transaction.status = 'cancelled'
            db.session.commit()
            emit('message', {'msg': 'Transaksi dibatalkan karena tidak ada kesepakatan.'}, room=data['room'])
            # Kirim notifikasi ke admin jika pembeli sudah mentransfer
            if transaction.amount > 0:
                # Logika untuk mengirim notifikasi ke admin
                pass

    socketio.start_background_task(cancel_transaction)
