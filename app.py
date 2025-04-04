from flask import Flask,render_template,url_for,redirect,request,flash,jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,Form
from wtforms.validators import DataRequired, Length

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///data.db'
app.config['SECRET_KEY'] ='key'

db=SQLAlchemy(app)
migrate=Migrate(app,db)

class CrrateJob(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired(), Length(min=10, max=50)])
    company = StringField('Company', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    description = StringField('Company Description', validators=[DataRequired()])
    no_employees = StringField('Number of Employees', validators=[DataRequired()])
    job_description = StringField('Job Description', validators=[DataRequired()])
    experience = StringField('Experience', validators=[DataRequired()])
    salary = StringField('Salary', validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    submit = SubmitField('Add Job')

# models
class Job(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    company = db.Column(db.String(100), nullable = False)
    location = db.Column(db.String(100), nullable = True)
    description = db.Column(db.String(500), nullable = False)
    experience = db.Column(db.String(100), nullable = False)
    salary = db.Column(db.String(100), nullable = False)
    type = db.Column(db.String(100), nullable = False)
    
    def _repr_(self):
        return f"{self.title}"
    
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=False)
    no_employees = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Company {self.name}>"

#routes
@app.route('/')
def jobs():
    jobs = Job.query.all()
    return render_template('jobs.html', jobs=jobs)
@app.route('/create', methods=['GET', 'POST'])
def create():
    form = CrrateJob()
    if form.validate_on_submit():
        # Check if the company already exists
        company = Company.query.filter_by(name=form.company.data).first()
        if not company:
            company = Company(
                name=form.company.data,
                description=form.description.data,
                no_employees=int(form.no_employees.data)
            )
            db.session.add(company)

        # Create the new job
        new_job = Job(
            title=form.title.data,
            company=company.name,
            location=form.location.data,
            description=form.job_description.data,
            experience=form.experience.data,
            salary=form.salary.data,
            type=form.type.data
        )
        db.session.add(new_job)
        db.session.commit()
        flash("Job is created successfully!")
        return redirect(url_for('jobs'))
    else:
        print(form.errors)
    return render_template('create_job.html', form=form)

@app.route('/job_details/<int:job_id>')
def job_details(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job_details.html', job=job)
@app.route('/company_details/<company_name>')
def company_details(company_name):
    company = Company.query.filter_by(name=company_name).first_or_404()
    jobs = Job.query.filter_by(company=company_name).all()
    return render_template('company_details.html', company=company, jobs=jobs)

@app.route('/delete/<int:job_id>', methods=['POST'])
def delete(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash("Job deleted successfully!")
    return redirect(url_for('jobs'))

@app.route('/update/<int:job_id>', methods=['GET', 'POST'])
def update(job_id):
    job = Job.query.get_or_404(job_id)

    form = CrrateJob(obj=job)  

    if form.validate_on_submit():
        job.title = form.title.data
        job.location = form.location.data
        job.description = form.job_description.data
        job.experience = form.experience.data
        job.salary = form.salary.data
        job.type = form.type.data

        company = Company.query.filter_by(name=job.company).first()
        if company:
            company.name = form.company.data
            company.description = form.description.data
            company.no_employees = int(form.no_employees.data)
        else:
            company = Company(
                name=form.company.data,
                description=form.description.data,
                no_employees=int(form.no_employees.data)
            )
            db.session.add(company)

        job.company = company.name

        db.session.commit()
        flash("Job updated successfully!")
        return redirect(url_for('jobs'))

    return render_template('update_job.html', form=form, job=job)