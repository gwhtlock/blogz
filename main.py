from flask import Flask, flash, redirect, render_template, request, session

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
#code on line below used to connect this program to a database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True # allows us to see the SQL in the terminal after the command has been completed
app.secret_key = 'ahduED43W' # secrect key used to denote a unque session


db = SQLAlchemy(app)


# model for the Task table in the database
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True) # creates a primary key denoted sequently after each task object is created
    title = db.Column(db.String(120))
    blog_post = db.Column(db.String(420))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    #creates a task object with name, owner data passed in the call of the task object
    def __init__(self, title, blog, owner):
        self.title = title
        self.blog_post = blog
        self.owner = owner


class User(db.Model):

    id= db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique = True)
    # email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120))
    blog = db.relationship('Blog', backref='owner')

    def __init__(self,username, password):
        # self.email = email
        self.username = username
        self.password = password

       




# class User(db.Model):

#     id= db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique = True)
#     password = db.Column(db.String(120))
#     task = db.relationship('Task', backref='owner')

#     def __init__(self,email, password):
#         self.email = email
#         self.password = password


@app.route('/', methods=['POST', 'GET'])
def index():

    # owner = User.query.filter_by(email=session['email']).first()    

    

        

        # removed list adder to accomdate database functionality
        # tasks.append(task_name)
    # tasks = Task.query.all() this query gets all items in the database
    # tasks = Task.query.filter_by(completed=False, owner=owner).all()
    # completed_tasks = Task.query.filter_by(completed=True, owner= owner).all()

    users = User.query.all()
    blog = Blog.query.all()

    return render_template('index.html',title="The Blog!", users=users)

@app.route('/newpost', methods=['POST', 'GET'])
def new_blog():
    title =""
    blog_body =""
    title_error = ""
    blog_error = ""

    # owner = User.query.filter_by(email=session['email']).first()
    owner = User.query.filter_by(username = session['username']).first()

    if request.method == 'POST':

        title = request.form['title']
        blog_body = request.form['body']

        if title == "":
            title_error = "You didnt add a title silly"

        if blog_body == "":
            blog_error = "You didnt add a blog post Ya big dummy"


        if title != "" and blog_body != "":
            new_blog = Blog(title, blog_body, owner)
            db.session.add(new_blog)
            db.session.commit()
            # all_blogs = Blog.query.all()
            the_blog = "/blog?id="+str(new_blog.id)
            return redirect(the_blog)

            # return render_template('mainblog.html',title="The Blog!", all_blogs = all_blogs)
    
    return render_template('blog.html',title="The Blog!", title_input = title, blog_body = blog_body, title_error = title_error, blog_error = blog_error)



@app.route('/blog', methods=['POST', 'GET'])
def see_the_blogs():

    # owner = User.query.filter_by(email=session['email']).first()
    blog_id = request.args.get('id')
    user_id = request.args.get('user')

    

    

    if  'username' not in session:

        if (blog_id):
            blog = Blog.query.get(blog_id)
            users = User.query.all()
            return render_template('oneblog.html',title="The Blog!", blog = blog, users = users)

        if(user_id):
            user_blogs = Blog.query.filter_by(owner_id = user_id).all()
            user = User.query.get(user_id)
            return render_template('mainblog.html',title="The Blog!", all_blogs = user_blogs, user = user)
        
        users = User.query.all()
        all_blogs = Blog.query.all()
        return render_template('mainblog.html',title="The Blog!", all_blogs = all_blogs, users = users)
    


    # filters all blogs to display only blogs for the current user
    # all_blogs = Blog.query.filter_by(owner = owner).all()
    
    owner = User.query.filter_by(username = session['username']).first()
    all_blogs = Blog.query.filter_by(owner = owner).all()

    # if(user_id):
    #     user_blogs = Blog.query.filter_by(user_id).all()
    #     return render_template('mainblog.html',title="The Blog!", all_blogs = user_blogs)


    blog_id = request.args.get('id')

    # if (blog_id):
    #     blog = Blog.query.get(blog_id)
    #     return render_template('oneblog.html',title="The Blog!", blog = blog)
    # if(user_id):
    #         user_blogs = Blog.query.filter_by(owner_id = user_id).all()
    #         return render_template('mainblog.html',title="The Blog!", all_blogs = user_blogs)


    # return render_template('mainblog.html',title="The Blog!", all_blogs = all_blogs)

    if (blog_id):
            blog = Blog.query.get(blog_id)
            users = User.query.all()
            return render_template('oneblog.html',title="The Blog!", blog = blog, users = users)

    if(user_id):
        user_blogs = Blog.query.filter_by(owner_id = user_id).all()
        user = User.query.get(user_id)
        return render_template('mainblog.html',title="The Blog!", all_blogs = user_blogs, user = user)
        
    users = User.query.all()
    all_blogs = Blog.query.all()
    return render_template('mainblog.html',title="The Blog!", all_blogs = all_blogs, users = users)




# @app.route('/delete-task', methods=['POST'])
# def delete_task():

#     task_id = int(request.form['task-id'])
#     task = Task.query.get(task_id)
#     task.completed = True

#     # removes the deletion of the task form the database
#     # db.session.delete(task)
#     db.session.add(task)
#     db.session.commit()

#     return redirect('/')


@app.before_request
def require_login():

    allowed_routes = ['login', 'register','see_the_blogs','index']

    if request.endpoint not in allowed_routes and 'username' not in session:
    # if request.endpoint not in allowed_routes and  not session:
        return redirect('/login')

@app.route('/login', methods=['POST','GET'])
def login():

    if request.method == 'POST':
    #    email = request.fo rm['email']
        username = request.form['username']
        password = request.form['password']
        # user = User.query.filter_by(email = email).first()
        user = User.query.filter_by(username = username).first()

        if user and user.password == password:
            #TODO remeber user has logined
            # session['email'] = email
            session['username'] = username
            flash("Logged In")
            print(session)
            return redirect('/newpost')
        elif not user:
            #TODO expalin why login failed
            flash('User does not exist', 'error')
        elif password != user.password:
            #TODO expalin why login failed
            flash('Incorrect Password', 'error')
            


    return render_template('login.html')


@app.route('/register', methods=['POST','GET'])
def register():

    flash_message =""
    if request.method == 'POST':
        # email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        verification =True
        

        #TODO validate user's data

        # existing_user = User.query.filter_by(email = email).first()
        existing_user = User.query.filter_by(username = username).first()

        if not username:
            flash_message += "No Username entered," + "     "
            verification = False
        elif len(username) <= 3:
            flash_message += "Username must be greater than 3 characters,"+ "     "
            verification = False
        elif existing_user:
            # TODO - Better User response
            flash_message += "Username already exists"+"     "
        
        
        if not password  or not verify:
            flash_message += "Must complete both password fields," + "     "
            verification = False
        elif len(password) <= 3:
            flash_message += "password must be greater than 3 characters,"+ "     "
            verification = False
        elif password != verify:
            flash_message += "The passwords do not match,"+ "     "
            verification = False

        

        if not existing_user and verification:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            #TODO - remeber the user
            # session['email'] = email
            session['username'] = username
            return redirect('/newpost')
        

    flash(flash_message)
    return render_template('register.html')


@app.route('/logout')
def logout():
    # del session['email']
    del session['username']
    return redirect('/')


if __name__ == '__main__':
    app.run()
