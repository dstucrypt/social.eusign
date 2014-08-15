from app import app as flask_app, db

if __name__ == '__main__':
    db.create_all()
    flask_app.run(debug=True, port=8001)
