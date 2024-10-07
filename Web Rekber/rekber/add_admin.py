from app import create_app, db
from app.models import User
from flask_bcrypt import generate_password_hash

app = create_app()
app.app_context().push()

hashed_password = generate_password_hash('Kikyrestu11152004!!!').decode('utf-8')
admin = User(username='admin', email='kimpulrestu@gmail.com', password=hashed_password, is_admin=True)
db.session.add(admin)
db.session.commit()
