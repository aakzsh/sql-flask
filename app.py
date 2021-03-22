from flask import render_template, Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'

db = SQLAlchemy(app)

class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<name %r>' % self.id


@app.route('/')
def index():
    title = "HomePage"
    return render_template("index.html", title=title)


@app.route('/friends', methods = ['POST', 'GET'])
def friends():
    title = "hello"
    if request.method == "POST":
        friend_name = request.form['name']
        new_friend = Friends(name=friend_name)

        #push

        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/friends')
        except:
            return "There was an error adding your friend lol"

    else:
        friends = Friends.query.order_by(Friends.date_created)
        return render_template("friends.html", title=title, friends=friends)





if __name__ == "__main__":
    app.run(debug=True)