from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from datetime import date
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField,IntegerField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import json

app = Flask(__name__)

# Config app secret key
app.config['SECRET_KEY'] = ''

# Config MySQL
app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''
app.config['MYSQL_CURSORCLASS'] = ''
# init MYSQL
mysql = MySQL(app)

 
# Index
@app.route('/')
def index():
    return render_template('home.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')


# Articles
@app.route('/challenges')
def articles():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM challenges")

    articles = cur.fetchall()

    if result > 0:
        return render_template('challenges.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('challenges.html', msg=msg)
    # Close connection
    cur.close()


#Single Article
@app.route('/challenge/<string:id>/', methods=['GET', 'POST'])
def article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article
    result = cur.execute("SELECT * FROM challenges WHERE ch_id = %s", [id])

    article = cur.fetchone()
    #Have flag ready 
    flag = article['ch_flag']
    if 'logged_in' in session:

        form = ArticleForm(request.form)
        

        #Check to see if the player has already solved this challenge before adding to their score
        cid = "$.c{0}".format(id)
        is_solved = cur.execute('SELECT flags->>%s as f FROM users WHERE username = %s ', (cid,[session['username']]))
        solved = cur.fetchall()
        

        if solved[0]['f'] is None:
            #Challenge was prob created after user account, easiest just to add it in real quick
            update_flags = cur.execute('UPDATE users set flags = JSON_SET(flags, %s, 0) WHERE username = %s', (cid,[session['username']]))
            #Grab the updated flags into the cursor
            is_solved = cur.execute('SELECT flags->>%s as f FROM users WHERE username = %s ', (cid,[session['username']]))
            solved = cur.fetchall()


        if request.method == 'POST' and form.validate():

            submitted_flag = request.form['flag']

            if submitted_flag == flag and int(solved[0]['f']) != 1:

                #Add the flag to the users so we can keep track of their challenges
                update_flags = cur.execute('UPDATE users set flags = JSON_SET(flags, %s, 1) WHERE username = %s', (cid,[session['username']]))
                mysql.connection.commit()

                #Update the users score to show they solved the challenge
                get_score = cur.execute('SELECT score FROM users WHERE username = %s', [session['username']])
                user_score = cur.fetchone()
                new_score = (int(user_score['score']) + int(article['ch_score']))
                updated_score = cur.execute('UPDATE users set score = %s WHERE username = %s', (new_score,[session['username']]))
                mysql.connection.commit()

                #Update the challenges number of solves
                get_solves = cur.execute('SELECT ch_solves from challenges WHERE ch_id = %s', ([id]))
                solves =  cur.fetchone()
                update_solves = int(solves['ch_solves']) + 1 
                updated_solves = cur.execute('UPDATE challenges set ch_solves = %s where ch_id =%s', (update_solves, [id]))
                mysql.connection.commit()

                flash('Good job! Your score has been updated','success')
                cur.close()
                return redirect(url_for('dashboard'))

            else:
                cur.close()
                flash('Incorrect answer', 'danger')
        cur.close()
        return render_template('challenge.html', article=article, form=form)
    else:
        cur.close()
        msg = 'Login to submit your answer!'
        return render_template('challenge.html', article=article, message=msg)


# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [
        validators.Length(min=6, max=50),
        validators.Email(message='Incorrect email format')
        ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        score = str(0)
        flags = {}
        # Create cursor
        cur = mysql.connection.cursor()

        challenges = cur.execute("SELECT * FROM challenges")
        challenges = cur.fetchall()
        for chal in challenges:
            key = 'c' + str(chal['ch_id'])
            flags[key] = 0
        flags = json.dumps(flags)
        
        cur.close()

        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password, score, flags, is_admin) VALUES(%s, %s, %s, %s, %s, %s,0)", (name, email, username, password, score, flags))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                session['admin'] = bool(data['is_admin'])

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM challenges")

    articles = cur.fetchall()

    # Get users scores to load onto page
    people = cur.execute("SELECT * from users ORDER BY score DESC")
    users = cur.fetchall()

    # Get completed challenges
    people = cur.execute("SELECT * from users WHERE username = %s", [session['username']])
    user = cur.fetchall()
    completed = user[0]['flags']
    comp_json = json.loads(completed)

    scores = []
    #Format everything up for the table
    for article in articles:
        score = {}
        score['ch_name']= article['ch_name']
        score['ch_score'] = article['ch_score']
        lookup = 'c'+ str(article['ch_id'])
        if lookup in comp_json:
            check = comp_json[lookup]
            if bool(check):
                score['ch_solved'] = True
            else:
                score['ch_solved'] = False
        else:
            score['ch_solved'] = False

        score['ch_solves'] = article['ch_solves']
        score['ch_category'] = article['ch_category']
        score['ch_difficulty'] = article['ch_difficulty']
        scores.append(score)



    if result > 0:
        return render_template('dashboard.html', users=users, scores=scores)
    else:
        msg = 'No Challenges Found'
        return render_template('dashboard.html', msg=msg)
    # Close connection
    cur.close()


# Add Article
@app.route('/add_challenge', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ChallengeForm(request.form)
    if request.method == 'POST' and form.validate():
        if session['admin']:
            ch_name = request.form['ch_name']
            ch_author = request.form['ch_author']
            ch_score = request.form['ch_score']
            ch_desc = request.form['ch_desc']
            ch_flag = request.form['ch_flag']
            ch_filepath = request.form['ch_filepath']
            ch_category = request.form['ch_category']
            ch_date = date.today()
            ch_solves=0
            ch_difficulty= request.form['ch_difficulty']
            # Create Cursor
            cur = mysql.connection.cursor()

            # Execute
            cur.execute("INSERT INTO challenges(ch_name, ch_author, ch_score, ch_desc, ch_date, ch_flag, ch_filepath, ch_category, ch_solves, ch_difficulty) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(ch_name, ch_author, ch_score, ch_desc, ch_date, ch_flag, ch_filepath, ch_category, ch_solves, ch_difficulty))

            # Commit to DB
            mysql.connection.commit()

            #Close connection
            cur.close()

            flash('Challenge Created', 'success')

            return redirect(url_for('dashboard'))

        else:
            flash('Invalid permissions, cant add challenge.', 'danger')
            app.logger.danger('Invalid operation requested, attempt to add challenge as non admin')
            return redirect(url_for('dashboard'))


    return render_template('add_challenge.html', form=form)


# Edit Article
@app.route('/edit_challenge/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_challenge(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article by id
    result = cur.execute("SELECT * FROM challenges WHERE ch_id = %s", [id])

    article = cur.fetchone()
    cur.close()
    # Get form
    form = ChallengeForm(request.form)

    # Populate article form fields
    form.ch_name.data = article['ch_name']
    form.ch_author.data = article['ch_author']
    form.ch_score.data = article['ch_score']
    form.ch_desc.data = article['ch_desc']
    form.ch_flag.data = article['ch_flag']
    form.ch_filepath.data = article['ch_filepath']
    form.ch_category.data = article['ch_category']
    form.ch_difficulty.data = article['ch_difficulty']
    if request.method == 'POST' and form.validate():
        if session['admin']:
            ch_name = request.form['ch_name']
            ch_author = request.form['ch_author']
            ch_score = request.form['ch_score']
            ch_desc = request.form['ch_desc']
            ch_flag = request.form['ch_flag']
            ch_filepath = request.form['ch_filepath']
            ch_category = request.form['ch_category']
            ch_difficulty = request.form['ch_difficulty']
            # Create Cursor
            cur = mysql.connection.cursor()
            app.logger.info(ch_name)
            # Execute
            cur.execute ("UPDATE challenges SET ch_name=%s, ch_author=%s, ch_score=%s, ch_desc=%s, ch_flag=%s, ch_filepath=%s, ch_category=%s, ch_difficulty=%s WHERE ch_id=%s",(ch_name, ch_author, ch_score, ch_desc, ch_flag, ch_filepath, ch_category, ch_difficulty, [id]))
            # Commit to DB
            mysql.connection.commit()

            #Close connection
            cur.close()

            flash('Challenge Updated', 'success')

            return redirect(url_for('dashboard'))

        else:
            flash('Action not permitted', 'danger')
            app.logger.danger('Invalid operation requested, attempt to modify challenge as non admin')
            return redirect(url_for('dashboard'))

    return render_template('edit_challenge.html', form=form)


# Delete Article
@app.route('/delete_challenge/<string:id>', methods=['GET','POST'])
@is_logged_in
def delete_challenge(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute
    if session['admin']:
        cur.execute("DELETE FROM challenges WHERE ch_id = %s", [id])
        flash('Challenge Deleted', 'success')
        # Commit to DB
        mysql.connection.commit()

    #Close connection
    cur.close()

    return redirect(url_for('dashboard'))

# Article Form Class
class ArticleForm(Form):
    flag = StringField('Flag', [validators.Length(min=1, max=200)])

class ChallengeForm(Form):
    ch_name = StringField('Name', [validators.Length(min=1, max=200)])
    ch_author = StringField('Author', [validators.Length(min=1, max=200)])
    ch_score = IntegerField('Score')
    ch_desc = TextAreaField('Description', [validators.Length(min=15)])
    ch_flag = StringField('Flag', [validators.Length(min=1, max=200)])
    ch_filepath = StringField('URL', [validators.Length(min=1, max=200)])
    ch_category = StringField('Category', [validators.Length(min=1, max=200)])
    ch_difficulty = StringField('Difficulty', [validators.Length(min=1,max=50)])

if __name__ == '__main__':
    app.run(debug=True)
