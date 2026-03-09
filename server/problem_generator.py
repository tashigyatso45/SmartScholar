"""
Free math problem generator for SmartScholars.
Sources:
  1. Programmatic generation (arithmetic, fractions, algebra, geometry, word problems)
  2. Open Trivia Database - category 19 (free, no API key required)
"""

import random
import math
import html
import json
import urllib.request
import urllib.error
from fractions import Fraction


# ── Formatting helpers ─────────────────────────────────────────────────────────

def _fmt(n):
    """Format a number: integer if whole, else 1 decimal place."""
    if isinstance(n, float) and n.is_integer():
        return str(int(n))
    elif isinstance(n, float):
        return f"{n:.1f}"
    return str(n)


def _frac_str(f):
    """Format a Fraction as '3/4' or '2' if denominator is 1."""
    if f.denominator == 1:
        return str(f.numerator)
    return f"{f.numerator}/{f.denominator}"


# ── Option builders ────────────────────────────────────────────────────────────

def _make_options(correct):
    """
    Build 4 unique answer options including the correct one.
    Returns (options: List[str], correct_str: str).
    """
    correct_str = _fmt(correct) if isinstance(correct, (int, float)) else str(correct)

    if not isinstance(correct, (int, float)):
        # String answer — caller should use _make_fraction_options instead
        options = ["10", "20", "30", correct_str]
        random.shuffle(options)
        return options, correct_str

    n = float(correct)
    mag = max(1, abs(n))

    if mag <= 12:
        offsets = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]
    elif mag <= 60:
        offsets = [-12, -8, -6, -5, -3, 3, 5, 6, 8, 10, 12]
    elif mag <= 200:
        offsets = [-20, -15, -10, -8, 8, 10, 15, 20, 25]
    else:
        step = max(5, int(mag * 0.08))
        offsets = [-step * 3, -step * 2, -step, step, step * 2, step * 3]

    random.shuffle(offsets)
    wrongs = []
    for off in offsets:
        if len(wrongs) == 3:
            break
        candidate = n + off
        if isinstance(correct, int):
            candidate = int(round(candidate))
        else:
            candidate = round(candidate, 1)
        s = _fmt(candidate)
        if s != correct_str and s not in wrongs and candidate > 0:
            wrongs.append(s)

    # Fallback: just increment
    i = 1
    while len(wrongs) < 3:
        candidate = correct + i
        s = _fmt(int(candidate) if isinstance(correct, int) else round(candidate, 1))
        if s != correct_str and s not in wrongs:
            wrongs.append(s)
        i += 1

    options = wrongs[:3] + [correct_str]
    random.shuffle(options)
    return options, correct_str


def _make_fraction_options(correct_frac):
    """Build 4 fraction-string options including correct_frac."""
    correct_str = _frac_str(correct_frac)
    wrongs = []
    attempts = 0
    while len(wrongs) < 3 and attempts < 40:
        dn = random.choice([-2, -1, 1, 2])
        dd = random.choice([-1, 0, 1])
        n = correct_frac.numerator + dn
        d = correct_frac.denominator + dd
        if n > 0 and d > 1:
            f = Fraction(n, d)
            s = _frac_str(f)
            if s != correct_str and s not in wrongs:
                wrongs.append(s)
        attempts += 1

    fallbacks = ["1/2", "2/3", "3/4", "1/4", "5/6", "1/3", "3/5", "4/5", "7/8", "2/5", "1/6"]
    for fb in fallbacks:
        if len(wrongs) >= 3:
            break
        if fb != correct_str and fb not in wrongs:
            wrongs.append(fb)

    options = wrongs[:3] + [correct_str]
    random.shuffle(options)
    return options, correct_str


# ── Arithmetic generators ──────────────────────────────────────────────────────

def _addition(difficulty, count):
    problems = []
    for _ in range(count):
        if difficulty == "easy":
            a, b = random.randint(1, 9), random.randint(1, 9)
        elif difficulty == "medium":
            a, b = random.randint(10, 59), random.randint(5, 39)
        else:
            a, b = random.randint(50, 499), random.randint(25, 199)
        correct = a + b
        options, cs = _make_options(correct)
        problems.append({
            "question": f"What is {a} + {b}?",
            "options": options,
            "correct_answer": cs,
            "explanation": f"Add the two numbers: {a} + {b} = {correct}.",
            "topic": "addition",
        })
    return problems


def _subtraction(difficulty, count):
    problems = []
    for _ in range(count):
        if difficulty == "easy":
            b = random.randint(1, 9)
            a = b + random.randint(1, 9)
        elif difficulty == "medium":
            b = random.randint(5, 39)
            a = b + random.randint(5, 49)
        else:
            b = random.randint(25, 199)
            a = b + random.randint(10, 150)
        correct = a - b
        options, cs = _make_options(correct)
        problems.append({
            "question": f"What is {a} - {b}?",
            "options": options,
            "correct_answer": cs,
            "explanation": f"Subtract {b} from {a}: {a} - {b} = {correct}.",
            "topic": "subtraction",
        })
    return problems


def _multiplication(difficulty, count):
    problems = []
    for _ in range(count):
        if difficulty == "easy":
            a, b = random.randint(1, 9), random.randint(1, 9)
        elif difficulty == "medium":
            a, b = random.randint(2, 12), random.randint(2, 12)
        else:
            a, b = random.randint(6, 25), random.randint(6, 20)
        correct = a * b
        options, cs = _make_options(correct)
        problems.append({
            "question": f"What is {a} \u00d7 {b}?",
            "options": options,
            "correct_answer": cs,
            "explanation": f"Multiply: {a} \u00d7 {b} = {correct}.",
            "topic": "multiplication",
        })
    return problems


def _division(difficulty, count):
    problems = []
    for _ in range(count):
        if difficulty == "easy":
            quotient, divisor = random.randint(1, 9), random.randint(2, 9)
        elif difficulty == "medium":
            quotient, divisor = random.randint(2, 15), random.randint(2, 12)
        else:
            quotient, divisor = random.randint(5, 30), random.randint(3, 15)
        dividend = quotient * divisor
        options, cs = _make_options(quotient)
        problems.append({
            "question": f"What is {dividend} \u00f7 {divisor}?",
            "options": options,
            "correct_answer": cs,
            "explanation": f"Divide: {dividend} \u00f7 {divisor} = {quotient}. Check: {divisor} \u00d7 {quotient} = {dividend}.",
            "topic": "division",
        })
    return problems


# ── Fractions ──────────────────────────────────────────────────────────────────

def _fractions(difficulty, count):
    problems = []
    if difficulty == "easy":
        types = ["add_same", "simplify"]
    elif difficulty == "medium":
        types = ["add_same", "simplify", "multiply", "add_different"]
    else:
        types = ["add_different", "multiply", "simplify", "mixed_number"]

    for _ in range(count):
        ptype = random.choice(types)

        if ptype == "add_same":
            d = random.choice([4, 6, 8, 10, 12])
            n1 = random.randint(1, d - 2)
            n2 = random.randint(1, d - 1 - n1)
            result = Fraction(n1 + n2, d)
            options, cs = _make_fraction_options(result)
            raw = f"{n1 + n2}/{d}"
            step = f" = {cs}" if cs != raw else ""
            problems.append({
                "question": f"What is {n1}/{d} + {n2}/{d}?",
                "options": options,
                "correct_answer": cs,
                "explanation": f"Same denominator — add numerators: ({n1}+{n2})/{d} = {raw}{step}.",
                "topic": "fraction addition",
            })

        elif ptype == "simplify":
            simple = random.choice([
                Fraction(1, 2), Fraction(1, 3), Fraction(2, 3),
                Fraction(1, 4), Fraction(3, 4), Fraction(2, 5), Fraction(3, 5),
            ])
            factor = random.randint(2, 4)
            big_n, big_d = simple.numerator * factor, simple.denominator * factor
            options, cs = _make_fraction_options(simple)
            problems.append({
                "question": f"Simplify the fraction {big_n}/{big_d}.",
                "options": options,
                "correct_answer": cs,
                "explanation": (
                    f"Both {big_n} and {big_d} share a factor of {factor}. "
                    f"{big_n}\u00f7{factor}={simple.numerator}, {big_d}\u00f7{factor}={simple.denominator}. "
                    f"Answer: {cs}."
                ),
                "topic": "simplifying fractions",
            })

        elif ptype == "multiply":
            f1 = random.choice([Fraction(1,2), Fraction(1,3), Fraction(2,3), Fraction(1,4), Fraction(3,4), Fraction(1,5)])
            f2 = random.choice([Fraction(1,2), Fraction(1,3), Fraction(2,3), Fraction(1,4), Fraction(3,4)])
            result = f1 * f2
            options, cs = _make_fraction_options(result)
            problems.append({
                "question": f"What is {_frac_str(f1)} \u00d7 {_frac_str(f2)}?",
                "options": options,
                "correct_answer": cs,
                "explanation": (
                    f"Multiply numerators and denominators: "
                    f"({f1.numerator}\u00d7{f2.numerator})/({f1.denominator}\u00d7{f2.denominator}) "
                    f"= {f1.numerator*f2.numerator}/{f1.denominator*f2.denominator} = {cs}."
                ),
                "topic": "fraction multiplication",
            })

        elif ptype == "add_different":
            pairs = [(Fraction(1,2), Fraction(1,3)), (Fraction(1,3), Fraction(1,4)),
                     (Fraction(1,2), Fraction(1,4)), (Fraction(2,3), Fraction(1,4)),
                     (Fraction(1,4), Fraction(1,6)), (Fraction(1,3), Fraction(1,6))]
            f1, f2 = random.choice(pairs)
            result = f1 + f2
            lcd = f1.denominator * f2.denominator // math.gcd(f1.denominator, f2.denominator)
            n1_adj = f1.numerator * (lcd // f1.denominator)
            n2_adj = f2.numerator * (lcd // f2.denominator)
            options, cs = _make_fraction_options(result)
            problems.append({
                "question": f"What is {_frac_str(f1)} + {_frac_str(f2)}?",
                "options": options,
                "correct_answer": cs,
                "explanation": (
                    f"Common denominator is {lcd}. "
                    f"{_frac_str(f1)} = {n1_adj}/{lcd}, {_frac_str(f2)} = {n2_adj}/{lcd}. "
                    f"Add: ({n1_adj}+{n2_adj})/{lcd} = {n1_adj+n2_adj}/{lcd} = {cs}."
                ),
                "topic": "fraction addition (different denominators)",
            })

        else:  # mixed_number
            whole = random.randint(1, 5)
            f = random.choice([Fraction(1,2), Fraction(1,3), Fraction(2,3), Fraction(1,4), Fraction(3,4)])
            result = Fraction(whole * f.denominator + f.numerator, f.denominator)
            options, cs = _make_fraction_options(result)
            problems.append({
                "question": f"Convert the mixed number {whole} {_frac_str(f)} to an improper fraction.",
                "options": options,
                "correct_answer": cs,
                "explanation": (
                    f"Multiply whole number by denominator and add numerator: "
                    f"({whole}\u00d7{f.denominator})+{f.numerator} = {whole*f.denominator+f.numerator}. "
                    f"Put over denominator: {cs}."
                ),
                "topic": "mixed numbers",
            })

    return problems


# ── Algebra ────────────────────────────────────────────────────────────────────

def _algebra(difficulty, count):
    problems = []
    for _ in range(count):
        if difficulty == "easy":
            form = random.choice(["add_eq", "sub_eq", "mult_eq"])
            x = random.randint(1, 12)
            a = random.randint(1, 10)
            if form == "add_eq":
                b = x + a
                problems.append({
                    "question": f"Solve for x: x + {a} = {b}",
                    "options": _make_options(x)[0],
                    "correct_answer": _make_options(x)[1],
                    "explanation": f"Subtract {a} from both sides: x = {b} - {a} = {x}.",
                    "topic": "one-step equations",
                })
            elif form == "sub_eq":
                b = x + a
                problems.append({
                    "question": f"Solve for x: x - {a} = {x - a if x > a else a}",
                    "options": _make_options(x)[0],
                    "correct_answer": _make_options(x)[1],
                    "explanation": f"Add {a} to both sides: x = {x - a if x > a else a} + {a} = {x}.",
                    "topic": "one-step equations",
                })
            else:
                m = random.randint(2, 5)
                b = m * x
                problems.append({
                    "question": f"Solve for x: {m}x = {b}",
                    "options": _make_options(x)[0],
                    "correct_answer": _make_options(x)[1],
                    "explanation": f"Divide both sides by {m}: x = {b} \u00f7 {m} = {x}.",
                    "topic": "one-step equations",
                })

        elif difficulty == "medium":
            x = random.randint(1, 15)
            m = random.randint(2, 5)
            a = random.randint(1, 10)
            b = m * x + a
            options, cs = _make_options(x)
            problems.append({
                "question": f"Solve for x: {m}x + {a} = {b}",
                "options": options,
                "correct_answer": cs,
                "explanation": (
                    f"Step 1: Subtract {a} from both sides \u2192 {m}x = {b} - {a} = {b - a}. "
                    f"Step 2: Divide by {m} \u2192 x = {b - a} \u00f7 {m} = {x}."
                ),
                "topic": "two-step equations",
            })

        else:
            x = random.randint(1, 10)
            a = random.randint(3, 8)
            c = random.randint(1, a - 1)
            b = random.randint(1, 15)
            d = (a - c) * x + b
            options, cs = _make_options(x)
            problems.append({
                "question": f"Solve for x: {a}x + {b} = {c}x + {d}",
                "options": options,
                "correct_answer": cs,
                "explanation": (
                    f"Move x terms left: {a}x - {c}x = {d} - {b} "
                    f"\u2192 {a - c}x = {d - b} "
                    f"\u2192 x = {d - b} \u00f7 {a - c} = {x}."
                ),
                "topic": "equations with variables on both sides",
            })

    return problems


# ── Geometry ───────────────────────────────────────────────────────────────────

PYTHAGOREAN_TRIPLES = [(3,4,5),(5,12,13),(8,15,17),(6,8,10),(9,12,15),(5,5,None)]

def _geometry(difficulty, count):
    problems = []
    for _ in range(count):
        if difficulty == "easy":
            shape = random.choice(["rect_area", "rect_perimeter", "square_area", "square_perimeter"])
        elif difficulty == "medium":
            shape = random.choice(["triangle_area", "circle_area", "box_volume", "rect_area"])
        else:
            shape = random.choice(["pythagorean", "circle_circumference", "surface_area", "triangle_area"])

        if shape == "rect_area":
            l, w = random.randint(2, 12), random.randint(2, 10)
            correct = l * w
            q = f"Find the area of a rectangle with length {l} and width {w}."
            ex = f"Area = length \u00d7 width = {l} \u00d7 {w} = {correct} square units."
            topic = "rectangle area"

        elif shape == "rect_perimeter":
            l, w = random.randint(2, 15), random.randint(2, 12)
            correct = 2 * (l + w)
            q = f"Find the perimeter of a rectangle with length {l} and width {w}."
            ex = f"Perimeter = 2 \u00d7 (l + w) = 2 \u00d7 ({l} + {w}) = 2 \u00d7 {l+w} = {correct} units."
            topic = "rectangle perimeter"

        elif shape == "square_area":
            s = random.randint(2, 12)
            correct = s * s
            q = f"Find the area of a square with side length {s}."
            ex = f"Area = side\u00b2 = {s} \u00d7 {s} = {correct} square units."
            topic = "square area"

        elif shape == "square_perimeter":
            s = random.randint(2, 15)
            correct = 4 * s
            q = f"Find the perimeter of a square with side length {s}."
            ex = f"Perimeter = 4 \u00d7 side = 4 \u00d7 {s} = {correct} units."
            topic = "square perimeter"

        elif shape == "triangle_area":
            b = random.randint(2, 15) * 2  # even base for clean division
            h = random.randint(2, 12)
            correct = (b * h) // 2
            q = f"Find the area of a triangle with base {b} and height {h}."
            ex = f"Area = (base \u00d7 height) \u00f7 2 = ({b} \u00d7 {h}) \u00f7 2 = {b*h} \u00f7 2 = {correct} sq units."
            topic = "triangle area"

        elif shape == "circle_area":
            r = random.randint(1, 7)
            raw = 3.14 * r * r
            correct = int(raw) if raw == int(raw) else round(raw, 1)
            q = f"Find the area of a circle with radius {r}. (Use \u03c0 \u2248 3.14)"
            ex = f"Area = \u03c0 \u00d7 r\u00b2 = 3.14 \u00d7 {r}\u00b2 = 3.14 \u00d7 {r*r} = {correct} sq units."
            topic = "circle area"

        elif shape == "box_volume":
            l, w, h = random.randint(2, 8), random.randint(2, 8), random.randint(2, 8)
            correct = l * w * h
            q = f"Find the volume of a box: length {l}, width {w}, height {h}."
            ex = f"Volume = l \u00d7 w \u00d7 h = {l} \u00d7 {w} \u00d7 {h} = {correct} cubic units."
            topic = "rectangular prism volume"

        elif shape == "pythagorean":
            a, b, c = random.choice([(3,4,5),(5,12,13),(8,15,17),(6,8,10),(9,12,15)])
            correct = c
            q = f"A right triangle has legs {a} and {b}. Find the hypotenuse."
            ex = f"c\u00b2 = a\u00b2 + b\u00b2 = {a}\u00b2 + {b}\u00b2 = {a*a} + {b*b} = {c*c}. So c = \u221a{c*c} = {c}."
            topic = "Pythagorean theorem"

        elif shape == "circle_circumference":
            r = random.randint(2, 9)
            raw = 2 * 3.14 * r
            correct = int(raw) if raw == int(raw) else round(raw, 1)
            q = f"Find the circumference of a circle with radius {r}. (Use \u03c0 \u2248 3.14)"
            ex = f"C = 2 \u00d7 \u03c0 \u00d7 r = 2 \u00d7 3.14 \u00d7 {r} = {correct} units."
            topic = "circle circumference"

        else:  # surface_area
            l, w, h = random.randint(2, 7), random.randint(2, 7), random.randint(2, 7)
            correct = 2 * (l*w + l*h + w*h)
            q = f"Find the surface area of a box: length {l}, width {w}, height {h}."
            ex = f"SA = 2(lw+lh+wh) = 2({l*w}+{l*h}+{w*h}) = 2\u00d7{l*w+l*h+w*h} = {correct} sq units."
            topic = "surface area"

        options, cs = _make_options(correct)
        problems.append({"question": q, "options": options, "correct_answer": cs, "explanation": ex, "topic": topic})
    return problems


# ── Word problem templates ─────────────────────────────────────────────────────

def _wp_apples():
    a, b = random.randint(5, 20), random.randint(2, 10)
    return {"question": f"You have {a} apples. Your friend gives you {b} more. How many do you have now?",
            "correct": a + b, "explanation": f"Add: {a} + {b} = {a+b}.", "topic": "addition word problems"}

def _wp_spend():
    start = random.randint(10, 30)
    spend = random.randint(2, start - 1)
    return {"question": f"You have ${start}. You spend ${spend}. How much is left?",
            "correct": start - spend, "explanation": f"Subtract: ${start} - ${spend} = ${start-spend}.", "topic": "subtraction word problems"}

def _wp_share():
    per = random.randint(2, 8)
    kids = random.randint(3, 8)
    total = per * kids
    return {"question": f"{total} cookies are shared equally among {kids} children. How many does each get?",
            "correct": per, "explanation": f"Divide: {total} \u00f7 {kids} = {per} cookies each.", "topic": "division word problems"}

def _wp_birds():
    total = random.randint(15, 40)
    flew = random.randint(3, total - 2)
    return {"question": f"There are {total} birds on a tree. {flew} fly away. How many remain?",
            "correct": total - flew, "explanation": f"Subtract: {total} - {flew} = {total-flew}.", "topic": "subtraction word problems"}

def _wp_bags():
    bags = random.randint(3, 8)
    per = random.randint(3, 9)
    return {"question": f"{bags} bags each hold {per} oranges. How many oranges total?",
            "correct": bags * per, "explanation": f"Multiply: {bags} \u00d7 {per} = {bags*per}.", "topic": "multiplication word problems"}

def _wp_rate():
    speed = random.randint(20, 70)
    hours = random.randint(2, 5)
    return {"question": f"A car travels at {speed} mph for {hours} hours. How far does it travel?",
            "correct": speed * hours, "explanation": f"Distance = speed \u00d7 time = {speed} \u00d7 {hours} = {speed*hours} miles.", "topic": "rate problems"}

def _wp_pct():
    pct = random.choice([10, 20, 25, 50])
    total = random.randint(4, 20) * (100 // pct)
    answer = total * pct // 100
    return {"question": f"What is {pct}% of {total}?",
            "correct": answer, "explanation": f"{pct}/100 \u00d7 {total} = {answer}.", "topic": "percentages"}

def _wp_multistep():
    budget = random.randint(20, 50)
    item1 = random.randint(5, 15)
    item2 = random.randint(3, min(10, budget - item1 - 1))
    spent = item1 + item2
    return {"question": f"You have ${budget}. You buy a book for ${item1} and a pen for ${item2}. How much is left?",
            "correct": budget - spent, "explanation": f"Spent: ${item1}+${item2}=${spent}. Left: ${budget}-${spent}=${budget-spent}.", "topic": "multi-step problems"}

def _wp_unit_rate():
    qty = random.randint(3, 8)
    unit = random.randint(2, 8)
    cost = qty * unit
    target = random.randint(2, 10)
    return {"question": f"If {qty} notebooks cost ${cost}, how much do {target} notebooks cost?",
            "correct": unit * target, "explanation": f"Unit price: ${cost}\u00f7{qty}=${unit}. For {target}: ${unit}\u00d7{target}=${unit*target}.", "topic": "unit rate"}

def _wp_reverse_rate():
    speed = random.randint(20, 80)
    hours = random.randint(2, 5)
    dist = speed * hours
    return {"question": f"A car traveled {dist} miles in {hours} hours. What was its average speed?",
            "correct": speed, "explanation": f"Speed = distance \u00f7 time = {dist} \u00f7 {hours} = {speed} mph.", "topic": "rate problems"}

def _wp_pct_increase():
    original = random.randint(4, 20) * 5
    pct = random.choice([10, 20, 25, 50])
    inc = original * pct // 100
    return {"question": f"A shirt costs ${original}. The price increases by {pct}%. What is the new price?",
            "correct": original + inc, "explanation": f"Increase = {pct}% \u00d7 ${original} = ${inc}. New = ${original}+${inc}=${original+inc}.", "topic": "percentage increase"}

def _wp_average():
    nums = [random.randint(10, 50) for _ in range(4)]
    avg = sum(nums) // 4
    return {"question": f"Find the average of: {', '.join(str(n) for n in nums)}.",
            "correct": avg, "explanation": f"Sum = {'+'.join(str(n) for n in nums)} = {sum(nums)}. Average = {sum(nums)}\u00f74 = {avg}.", "topic": "averages"}


def _word_problems(difficulty, count):
    easy = [_wp_apples, _wp_spend, _wp_share, _wp_birds, _wp_bags]
    medium = [_wp_rate, _wp_pct, _wp_multistep, _wp_unit_rate, _wp_reverse_rate]
    hard = [_wp_pct_increase, _wp_average, _wp_unit_rate, _wp_reverse_rate, _wp_multistep]
    pool = easy if difficulty == "easy" else medium if difficulty == "medium" else hard

    problems = []
    for _ in range(count):
        p = random.choice(pool)()
        options, cs = _make_options(p["correct"])
        problems.append({
            "question": p["question"],
            "options": options,
            "correct_answer": cs,
            "explanation": p["explanation"],
            "topic": p["topic"],
        })
    return problems


# ── Open Trivia DB ─────────────────────────────────────────────────────────────

def _fetch_open_trivia(difficulty, count):
    """
    Fetch math trivia from Open Trivia Database (category 19, free, no key).
    Raises on network failure or bad response.
    """
    url = (
        f"https://opentdb.com/api.php"
        f"?amount={count}&category=19&difficulty={difficulty}&type=multiple"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "SmartScholars/1.0"})
    with urllib.request.urlopen(req, timeout=6) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    if data.get("response_code") != 0 or not data.get("results"):
        raise ValueError(f"OpenTDB response_code={data.get('response_code')}")

    problems = []
    for item in data["results"]:
        question = html.unescape(item["question"])
        correct = html.unescape(item["correct_answer"])
        wrongs = [html.unescape(w) for w in item["incorrect_answers"]]
        options = wrongs + [correct]
        random.shuffle(options)
        problems.append({
            "question": question,
            "options": options,
            "correct_answer": correct,
            "explanation": f"The correct answer is: {correct}.",
            "topic": "math trivia",
        })
    return problems


# ── Subject router ─────────────────────────────────────────────────────────────

_SUBJECT_MAP = {
    "addition":         _addition,
    "subtraction":      _subtraction,
    "multiplication":   _multiplication,
    "division":         _division,
    "fractions":        _fractions,
    "fractions and decimals": _fractions,
    "algebra":          _algebra,
    "geometry":         _geometry,
    "word problems":    _word_problems,
}


def generate_problems(subject, difficulty, count):
    """
    Main entry point. Routes to the right generator by subject name.
    Falls back to Open Trivia DB for unknown subjects, then to addition.
    Always returns exactly `count` problem dicts with keys:
      question, options (list of 4 str), correct_answer, explanation, topic.
    """
    key = subject.lower().strip()
    generator = _SUBJECT_MAP.get(key)

    if generator:
        return generator(difficulty, count)

    # Unknown subject — try trivia, fall back to addition
    try:
        problems = _fetch_open_trivia(difficulty, count)
        if problems:
            return problems[:count]
    except Exception:
        pass

    return _addition(difficulty, count)
