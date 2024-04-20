from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    surname = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    patronymic = db.Column(db.String(100))
    university = db.Column(db.String(100), nullable=False)
    course = db.Column(db.Integer, nullable=False)


@app.route('/')
def index():
    return render_template('registration.html')


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        surname = request.form['surname']
        name = request.form['name']
        patronymic = request.form['patronymic']
        university = request.form['university']
        course = request.form['course']

        new_student = Student(surname=surname, name=name, patronymic=patronymic, university=university, course=course)
        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for('student_profile', student_id=new_student.id))


@app.route('/student_profile/<int:student_id>')
def student_profile(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student_profile.html', student=student)


if __name__ == '__main__':
    app.run(debug=True)
