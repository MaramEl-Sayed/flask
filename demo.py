# from flask import Flask, request, render_template

# app = Flask(__name__)

# @app.route('/<name>')
# def index(name):
#     return f"<p>Hello, {name}!</p>"

# @app.route('/users', methods = ['GET', 'POST'])
# def users():
#     users = {
#         "sayed": "sayed@iti.com",
#         "ahmed": "ahmed@iti.com",
#         "mohamed": "mohamed@iti.com",
#         "nour": "nour@iti.com"
#     }
#     if request.method == 'GET':
#         return f"{users}"
#     elif request.method == 'POST':
#         return 'Cannot Post Data Here'

# @app.route("/hello")
# def hello():
#     name = "iTi Students"
#     sayed = 'sayed'
#     return render_template('hello.html', name=name, current_user= sayed)


# from flask import Flask, render_template

# app = Flask(_name_)

# @app.route('/jobs')
# def jobs():
#     jobs = [
#         {
#             "id": 1,
#             "title": "Software Engineer",
#             "company": "Vodafon",
#             "location": "Smart Village"
            
#         },
#         {
#             "id": 2,
#             "title": "FrontEnd Engineer",
#             "company": "DXC",
#             "location": "Smart Village"
            
#         },
#         {
#             "id": 3,
#             "title": "BackEnd Engineer",
#             "company": "PWC",
#             "location": "Tagamoa"
            
#         },
#         {
#             "id": 4,
#             "title": "Mobile App Developer",
#             "company": "b_labs",
#             "location": "Qattamia"
            
#         },
#     ]
    
#     return render_template('jobs.html', jobs=jobs)

# # Job Details Page (add job (name, discription, needed experience,  salary, type(fultime or part)))
# # company Details page (company name, discrption, employees count)




# from flask import Flask, render_template, redirect, url_for
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired, Length, Email

# app = Flask(_name_)
# app.config['SECRET_KEY'] = 'your secret'

# class RegistrationForm(FlaskForm):
#     username = StringField('UserName', validators=[DataRequired(), Length(min=4, max=50)])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Register')

# @app.route('/')
# def home():
#     return "Welcome To Our App"

# @app.route('/register', methods = ['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit(): #POST
#         return redirect(url_for('home'))
#     return render_template('register.html', form=form) # GET



from flask import Flask, request, render_template, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # database config for connection
app.config['SECRET_KEY'] = "my secret"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# models
class Job(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    company = db.Column(db.String(100), nullable = False)
    location = db.Column(db.String(100), nullable = True)
    
    def _repr_(self):
        return f"{self.title}"
    
# Need To Create Form For job creation

@app.route('/jobs')
def jobs():
    jobs = Job.query.all()
    return render_template('jobs.html', jobs=jobs)

@app.route('/job/create', methods = ['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        location = request.form['location']
        
        if not title or not company:
            flash("Title And Company Fields Are Required")
            return redirect(url_for('create'))
        
        new_job = Job(title=title, company=company, location=location)
        db.session.add(new_job)
        db.session.commit()
        
        flash("Job Is Created Successfully!")
        return redirect(url_for('jobs'))
    
    return render_template('create_job.html')

# job details and company details routes need to be created and company model


# APIs
@app.route('/api/jobs', methods = ['GET'])
def get_jobs():
    jobs = Job.query.all()
    print("*"*100)
    print(jobs)
    print("*"*100)
    data = []
    for job in jobs:
        _job = {}
        _job['id'] = job.id
        _job['title'] = job.title
        _job['company'] = job.company
        _job['location'] = job.location
        data.append(_job)
    return jsonify(data)

@app.route('/api/job/<id>', methods=['GET'])
def get_job(id):
    job = Job.query.get_or_404(id= int(id))
    data = {
        'id': job.id,
        'title': job.title,
        'company': job.company,
        'location': job.location
    }
    return jsonify(data)

@app.route('/api/job/update/<id>', methods = ['PUT'])
def update_job(id):
    job = Job.query.get_or_404(id)
    if request.method == 'PUT':
        data = request.get_json()
        job.title = data['title']
        job.company = data['company']
        job.location = data['location']
        
        db.session.commit()
        return jsonify({'Message': 'Job Updated!'})
    
@app.route('/api/job/delete/<id>', methods = ['DELETE'])
def delete_job(id):
    job = Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    
    return jsonify({"Message": "Job Deleted!"})