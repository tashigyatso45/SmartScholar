#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Subject, Answer, Card_Deck, Question_Card, Question
import json 

if __name__ == '__main__':
    faker = Faker()


def create_users():
    users = []
    for _ in range(10):
        u = User (
            username = faker.user_name(),
            _password_hash = faker.password(),
            email = faker.email(),
            grade_level = faker.random_int(min=1, max=3)
        )   
        users.append(u)
    return users

def create_questions():
    questions = []

    for _ in range(10):
        num1 = faker.random_int(min=1, max=10)
        num2 = faker.random_int(min=1, max=10)
        operator = faker.random_element(elements=['+', '-', '*', '/'])
        math_problem = f"{num1} {operator} {num2}"
        result = eval(math_problem)

        content_json = json.dumps({
            'num1': num1,
            'num2': num2,
            'math_problem': math_problem,
            'result': result
        })


        q = Question(
        content= content_json,
        correct_answer = result
        )
        questions.append(q)
    return questions 

    
    subjects= []

    s1 = Subject(type_operation='Division')
    subjects.append(s1)

    s2 = Subject(type_operation='Addition')
    subjects.append(s2)
    s3= Subject(type_operation='Subtraction')
    subjects.append(s3)
    s4= Subject(type_operation='Multiplication')
    subjects.append(s4)
    db.session.add_all(subjects)
    db.session.commit()



def create_card_deck(users):
    card_decks = []
    for _ in range(10):
        c = Card_Deck(
            user_id = rc([user.id for user in users])
        )
        card_decks.append(c)
    return card_decks

def create_question_card(card_decks, questions):
    question_cards = []
    for _ in range(10):
        q = Question_Card(
            is_complete =faker.boolean(),
            card_deck_id = rc([card_deck.id for card_deck in card_decks]),
            question_id= rc([question.id for question in questions])
        )
        question_cards.append(q)
    return question_cards

def create_answers(users, question_cards):
    answers = []
    for _ in range(10):
        a = Answer(
            user_answer = faker.random_int(),
            is_correct = faker.boolean(),
            user_id = rc([user.id for user in users]),
            question_card_id = rc ([question_card.id for question_card in question_cards])
        )
        answers.append(a)
    return answers




if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")
        User.query.delete()
        Answer.query.delete()
        Card_Deck.query.delete()
        Question_Card.query.delete()
        Question.query.delete()

        print("Seeding gyms...")
        users = create_users()
        db.session.add_all(users)
        db.session.commit()

    
        print("Seeding reviews...")
        card_decks = create_card_deck(users)
        db.session.add_all(card_decks)
        db.session.commit()

        print("Seeding reviews...")
        questions = create_questions()
        db.session.add_all(questions)
        db.session.commit()

        print("Seeding reviews...")
        question_cards = create_question_card(card_decks, questions)
        db.session.add_all(question_cards)
        db.session.commit()

        print("Seeding users...")
        answers = create_answers(question_cards, users)
        db.session.add_all(answers)
        db.session.commit()

        print("Done seeding!")




























