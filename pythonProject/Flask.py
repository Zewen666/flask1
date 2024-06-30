# Import necessary libraries
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, RadioField
from wtforms.validators import DataRequired
import subprocess

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Configure the secret key for Flask-WTF


# Define the questionnaire form class
class QuestionnaireForm(FlaskForm):
    short_term = StringField('Short Term Goals', validators=[DataRequired()])  # Short term goals field
    long_term = TextAreaField('Long Term Goals', validators=[DataRequired()])  # Long term goals field
    choices = RadioField('Choices', choices=[('opt1', 'Option 1'), ('opt2', 'Option 2')],
                         validators=[DataRequired()])  # Choices field


# Define the home page route
@app.route('/')
def home():
    return render_template('home.html')  # Render home.html template


# Define the about page route
@app.route('/about')
def about():
    return render_template('about.html')  # Render about.html template


# Define the questionnaire page route
@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    form = QuestionnaireForm()  # Create an instance of the questionnaire form
    if form.validate_on_submit():  # If the form is validated
        # Write the form data to a data.txt file
        with open('data.txt', 'a') as f:
            f.write(
                f"Short Term: {form.short_term.data}\nLong Term: {form.long_term.data}\nChoice: {form.choices.data}\n")

        # Git integration: add, commit and push the changes
        subprocess.run(['git', 'add', 'data.txt'])
        subprocess.run(['git', 'commit', '-m', 'Update data.txt with new form submission'])
        subprocess.run(['git', 'push'])

        return 'Form Submitted!'  # Return a success message
    return render_template('questionnaire.html',
                           form=form)  # Render the questionnaire template and pass the form instance


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode
