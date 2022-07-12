from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []

@app.route("/")
def go_homepage():
    """shows home page"""
    return render_template("home.html", survey_title = survey.title, survey_instruction = survey.instructions)

@app.route("/questions/<int:idx>")
def go_question(idx):
    if len(responses) != idx and len(responses) < len(survey.questions):
        flash("Cannot access an invalid question")
        return redirect(f"/questions/{len(responses)}")
    elif len(responses) >= len(survey.questions):
        print("finish-1")
        return redirect("/finished")
    else:
        questions = survey.questions
        return render_template("question.html", idx = idx, question = questions[idx], survey_title = survey.title)

@app.route("/answer", methods=["POST"])
def handle_question():
    if len(responses) == len(survey.questions):
        print("finish-2")
        return redirect("/finished")
    else:
        answer = request.form['answer']
        responses.append(answer)
        return redirect(f"/questions/{len(responses)}")

@app.route("/finished")
def finish_page():
    return render_template("finished.html", responses=responses)



    # satisfaction_survey = Survey(
    # "Customer Satisfaction Survey",
    # "Please fill out a survey about your experience with us.",
    # [
    #     Question("Have you shopped here before?"),
    #     Question("Did someone else shop with you today?"),
    #     Question("On average, how much do you spend a month on frisbees?",
    #              ["Less than $10,000", "$10,000 or more"]),
    #     Question("Are you likely to shop here again?"),
    # ])