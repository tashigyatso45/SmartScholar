#!/usr/bin/env python3

import os
import json
import random

from flask import request, make_response, session
from flask_restful import Resource

from config import app, db, api
from models import User, Subject, Answer, Card_Deck, Question, Question_Card, GeneratedProblem
from problem_generator import generate_problems as _generate_free


# ─── Helpers ───────────────────────────────────────────────────────────────────

def problem_to_dict(p):
    """Serialize a GeneratedProblem, parsing the options JSON string to a list."""
    return {
        "id": p.id,
        "subject": p.subject,
        "difficulty": p.difficulty,
        "question": p.question,
        "options": json.loads(p.options),
        "correct_answer": p.correct_answer,
        "explanation": p.explanation,
        "topic": p.topic,
        "created_at": p.created_at.isoformat() if p.created_at else None,
    }



# ─── Auth routes ───────────────────────────────────────────────────────────────

class Users(Resource):
    def post(self):
        data = request.get_json()
        user = User(
            username=data["username"],
            password_hash=data["password"],
            email=data["email"],
            grade_level=data["grade_level"],
        )
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        return make_response({"user": user.to_dict()}, 201)


api.add_resource(Users, "/api/v1/register")


@app.route("/api/v1/authorized")
def authorized():
    try:
        user = User.query.filter_by(id=session.get("user_id")).first()
        return make_response(user.to_dict(), 200)
    except:
        return make_response({"error": "User not found"}, 404)


@app.route("/api/v1/logout", methods=["DELETE"])
def logout():
    session["user_id"] = None
    return make_response({}, 201)


@app.route("/api/v1/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    user = User.query.filter_by(username=data.get("username")).first()
    if user and user.authenticate(data.get("password", "")):
        session["user_id"] = user.id
        return make_response({"user": user.to_dict()}, 201)
    return make_response({"error": "Invalid credentials"}, 401)


# ─── Subjects ──────────────────────────────────────────────────────────────────

class Subjects(Resource):
    def get(self):
        subjects = [subject.to_dict() for subject in Subject.query.all()]
        return make_response(subjects, 200)


api.add_resource(Subjects, "/api/v1/home")


# ─── Question Cards ────────────────────────────────────────────────────────────

class Question_Cards(Resource):
    def get(self):
        question_cards = [card_deck.to_dict() for card_deck in Question_Card.query.all()]
        return make_response(question_cards, 200)


api.add_resource(Question_Cards, "/api/v1/question_card")


# ─── AI-Generated Problems ─────────────────────────────────────────────────────

@app.route("/api/v1/problems", methods=["GET"])
def get_problems():
    """Return cached problems filtered by subject and difficulty."""
    subject = request.args.get("subject")
    difficulty = request.args.get("difficulty", "easy")
    count = int(request.args.get("count", 5))

    if not subject:
        return make_response({"error": "subject query param is required"}, 400)

    problems = GeneratedProblem.query.filter_by(
        subject=subject, difficulty=difficulty
    ).all()

    if len(problems) >= count:
        selected = random.sample(problems, count)
        return make_response([problem_to_dict(p) for p in selected], 200)

    return make_response([problem_to_dict(p) for p in problems], 200)


@app.route("/api/v1/problems/generate", methods=["POST"])
def generate_problems():
    """Generate fresh problems using the free local generator and cache them."""
    data = request.get_json() or {}
    subject = data.get("subject")
    difficulty = data.get("difficulty", "easy")
    count = int(data.get("count", 5))

    if not subject:
        return make_response({"error": "subject is required"}, 400)

    try:
        problems_data = _generate_free(subject, difficulty, count)
        saved = []
        for p in problems_data:
            problem = GeneratedProblem(
                subject=subject,
                difficulty=difficulty,
                question=p["question"],
                options=json.dumps(p["options"]),
                correct_answer=p["correct_answer"],
                explanation=p["explanation"],
                topic=p.get("topic", subject),
            )
            db.session.add(problem)
            saved.append(problem)
        db.session.commit()
        return make_response([problem_to_dict(p) for p in saved], 201)
    except Exception as e:
        return make_response({"error": f"Failed to generate problems: {str(e)}"}, 500)


# ─── Index ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return "<h1>SmartScholars Server</h1>"


if __name__ == "__main__":
    app.run(port=5555, debug=True)
