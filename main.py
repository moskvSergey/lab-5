from sqlalchemy import create_engine, not_, and_, or_,func
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from models import Department, User, Jobs, Base
from sqlalchemy.exc import IntegrityError

'''
def add_people(session):
    captain = User(
        surname='Scott',
        name='Ridley',
        age=21,
        position='captain',
        speciality='research engineer',
        address='module_1',
        email='scott_chief@mars.org',
    )

    colonists = [
        User(surname='Surname1', name='Name1', age=30, position='Major',
             speciality='research engineer', address='module_1', email='email1@example.com'),
        User(surname='Surname2', name='Name2', age=34, position='Major',
             speciality='mechanic', address='module_1', email='email2@example.com'),
        User(surname='Surname3', name='Name3', age=29, position='Sergant',
             speciality='geological engineer', address='module_1', email='email3@example.com'),
        User(surname='Surname4', name='Name4', age=40, position='Sergant',
             speciality='physic', address='module_2', email='email4@example.com'),
        User(surname='Surname5', name='Name5', age=17, position='chief',
             speciality='clean engineer', address='module_2', email='email5@example.com'),
    ]

    session.add(captain)
    session.add_all(colonists)
    session.commit()

def add_jobs(session):
    new_job = Jobs(
        team_leader=1,
        job='deployment of residential modules 1 and 2',
        work_size=15,
        collaborators='2, 3',
        start_date=datetime.now(),
        is_finished=False,
    )

    session.add(new_job)
    session.commit()

def add_depart(session):
    new_dep = Department(
        id=1,
        title="Research Dep",
        chief=1,
        members='1,2,3',
        email="dep1@mail.ru"
    )

    session.add(new_dep)
    session.commit()

def do_something(func):
    database_name = "mars_explorer"#input("Введите имя базы данных: ")
    engine = create_engine(f'sqlite:///{database_name}.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return func(session)


def zad_4(session):
    colonists = session.query(User).filter(User.address == 'module_1').all()
    for colonist in colonists:
        print(colonist)


def zad_5(session):
    colonists = session.query(User).filter(
        and_(
            User.address == 'module_1',
            not_(User.speciality.contains('engineer')),
            not_(User.position.contains('engineer'))
        )
    ).all()

    for colonist in colonists:
        print(colonist.id)


def zad_6(session):
    underage_colonists = session.query(User).filter(User.age < 18).all()

    for colonist in underage_colonists:
        print(f"{colonist.name} {colonist.surname}, возраст: {colonist.age} лет")

def zad_7(session):
    colonists_with_positions = session.query(User).filter(
        or_(
            User.position.contains('chief'),
            User.position.contains('middle')
        )
    ).all()

    for colonist in colonists_with_positions:
        print(f"{colonist.id} {colonist.surname} {colonist.name}, должность: {colonist.position}")


def zad_8(session):
    jobs = session.query(Jobs).filter(Jobs.work_size < 20, Jobs.is_finished == False).all()

    for job in jobs:
        print(job)

def zad_9(session):
    max_team_size = session.query(
        func.max(func.length(Jobs.collaborators) - func.length(func.replace(Jobs.collaborators, ',', '')))).scalar() + 1
    jobs_with_largest_teams = session.query(Jobs).filter(func.length(Jobs.collaborators) - func.length(
        func.replace(Jobs.collaborators, ',', '')) + 1 == max_team_size).all()

    team_leads_ids = [job.team_leader for job in jobs_with_largest_teams]
    team_leads = session.query(User).filter(User.id.in_(team_leads_ids)).all()

    for lead in team_leads:
        print(f"{lead.surname} {lead.name}")

def zad_10(session):
    session.query(User).filter(User.address == 'module_1',
                               User.age < 21).update({"address": "module_3"})


def zad_12(session):#Находит суммарные трудозатраты на работу
    department = session.query(Department).filter(Department.id == 1).first()
    if department is None:
        print(f"Департамент с id {1} не найден.")
        return
    member_ids = department.members.split(',')

    total_hours = 0
    job = session.query(Jobs).filter(Jobs.id == 1).first()
    for member_id in member_ids:
        user = session.query(User).filter(User.id == member_id).first()
        if user:
            total_hours += job.work_size

    print(total_hours)
'''

app = Flask(__name__)
engine = create_engine('sqlite:///mars_explorer.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def jobs_list():
    jobs = session.query(Jobs).all()
    return render_template('jobs.html', jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        surname = request.form['surname']
        name = request.form['name']
        age = request.form['age']
        position = request.form['position']
        speciality = request.form['speciality']
        address = request.form['address']
        email = request.form['email']

        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Пароли не совпадают."

        new_user = User(surname=surname, name=name, hashed_password=password,
                        age=age, position=position, speciality=speciality,
                        address=address, email=email)

        session.add(new_user)
        try:
            session.commit()
            return redirect(url_for('jobs_list'))
        except IntegrityError:
            session.rollback()
            return "Ошибка: Пользователь с такими данными уже существует"

    return render_template('register.html')


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        new_job = Jobs(
            team_leader=request.form['team_leader'],
            job=request.form['job'],
            work_size=request.form['work_size'],
            collaborators=request.form['collaborators']
        )
        session.add(new_job)
        session.commit()
        return redirect(url_for('add_job'))

    return render_template('add_jobs.html')


@app.route('/add_department', methods=['GET', 'POST'])
def add_department():
    if request.method == 'POST':
        new_department = Department(
            title=request.form['title'],
            chief=request.form['chief'],
            members=request.form['members'],
            email=request.form['email']
        )
        session.add(new_department)
        session.commit()
        return redirect(url_for('add_department'))  # Или куда вам нужно перенаправить после добавления отдела
    return render_template('department.html')


if __name__ == '__main__':
    app.run(debug=True)
