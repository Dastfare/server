from flask import Flask, request, render_template
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Определение модели данных
Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    surname = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    patronymic = Column(String(255))
    university = Column(String(255), nullable=False)
    course = Column(Integer, nullable=False)

# Создание подключения к базе данных
engine = create_engine('sqlite:///students.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Обработчик маршрута регистрации студента
@app.route('/submit_registration', methods=['POST'])
def submit_registration():
    # Получение данных из формы
    surname = request.form['surname']
    name = request.form['name']
    patronymic = request.form['patronymic']
    university = request.form['university']
    course = int(request.form['course'])

    # Создание объекта Student и добавление его в базу данных
    new_student = Student(surname=surname, name=name, patronymic=patronymic, university=university, course=course)
    session.add(new_student)
    session.commit()

    return 'Студент успешно добавлен в базу данных.'

if __name__ == '__main__':
    app.run(debug=True)
