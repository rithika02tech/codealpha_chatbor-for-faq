from flask import Flask, render_template, request, jsonify
import pandas as pd
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)


faq_data = pd.read_csv("faq.csv")

faq_data["question"] = faq_data["question"].astype(str)
faq_data["answer"] = faq_data["answer"].astype(str)

questions = faq_data["question"].tolist()
answers = faq_data["answer"].tolist()


categories = {

    "wifi": [
        "wifi", "internet", "router",
        "network", "hotspot", "ethernet",
        "signal"
    ],

    "login": [
        "password", "login", "account",
        "credentials"
    ],

    "laptop": [
        "laptop", "computer", "battery",
        "slow", "fan", "freeze"
    ],

    "software": [
        "software", "install",
        "application", "program"
    ],

    "printer": [
        "printer", "printing",
        "paper", "scan", "offline"
    ],

    "audio": [
        "audio", "sound",
        "microphone", "speaker"
    ],

    "phone": [
        "phone", "mobile",
        "android", "charger"
    ],

    "email": [
        "email", "mail",
        "spam", "attachment"
    ]
}


current_category = ""


def preprocess(text):

    text = text.lower()

    text = "".join(
        char for char in text
        if char not in string.punctuation
    )

    return text


def detect_category(user_input):

    user_input = preprocess(user_input)

    for category, keywords in categories.items():

        for keyword in keywords:

            if keyword in user_input:
                return category

    return None


def get_related_questions(category, current_question):

    related = []

    if category not in categories:
        return related

    keywords = categories[category]

    for q in questions:

        q_clean = preprocess(q)

        if current_question.lower() not in q.lower():

            for keyword in keywords:

                if keyword in q_clean:

                    related.append(q)

                    break

    return related[:4]


def get_faq_response(user_input, category=None):

    processed_questions = [
        preprocess(q)
        for q in questions
    ]

    processed_input = preprocess(user_input)

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        processed_questions + [processed_input]
    )

    similarity = cosine_similarity(
        vectors[-1],
        vectors[:-1]
    )

    best_match_index = similarity.argmax()

    best_score = similarity[0][best_match_index]

    if best_score > 0.15:

        matched_question = questions[best_match_index]

        answer = answers[best_match_index]

        related = get_related_questions(
            category,
            matched_question
        )

        return answer, related

    return (
        "Sorry, I couldn't fully understand your issue. "
        "Please try describing it differently."
    ), []


@app.route("/")
def home():

    return render_template("index.html")



@app.route("/get")
def chatbot():

    global current_category

    user_input = request.args.get("msg")

    # DETECT CATEGORY

    detected = detect_category(user_input)

    if detected:
        current_category = detected

   

    answer, related = get_faq_response(
        user_input,
        current_category
    )

    

    related_html = ""

    if related:

        related_html += """
        <div class='related-title'>
            Related Issues
        </div>

        <div class='related-container'>
        """

        for item in related:

            related_html += f"""
            <button
                class='related-btn'
                onclick="sendRelated(`{item}`)"
            >
                {item}
            </button>
            """

        related_html += "</div>"

    final_response = f"""
    {answer}
    {related_html}
    """

    return jsonify(response=final_response)



from flask import Flask, render_template, request, jsonify
import pandas as pd
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)



faq_data = pd.read_csv("faq.csv")

faq_data["question"] = faq_data["question"].astype(str)
faq_data["answer"] = faq_data["answer"].astype(str)

questions = faq_data["question"].tolist()
answers = faq_data["answer"].tolist()



categories = {

    "wifi": [
        "wifi", "internet", "router",
        "network", "hotspot", "ethernet",
        "signal"
    ],

    "login": [
        "password", "login", "account",
        "credentials"
    ],

    "laptop": [
        "laptop", "computer", "battery",
        "slow", "fan", "freeze"
    ],

    "software": [
        "software", "install",
        "application", "program"
    ],

    "printer": [
        "printer", "printing",
        "paper", "scan", "offline"
    ],

    "audio": [
        "audio", "sound",
        "microphone", "speaker"
    ],

    "phone": [
        "phone", "mobile",
        "android", "charger"
    ],

    "email": [
        "email", "mail",
        "spam", "attachment"
    ]
}



current_category = ""



def preprocess(text):

    text = text.lower()

    text = "".join(
        char for char in text
        if char not in string.punctuation
    )

    return text


def detect_category(user_input):

    user_input = preprocess(user_input)

    for category, keywords in categories.items():

        for keyword in keywords:

            if keyword in user_input:
                return category

    return None



def get_related_questions(category, current_question):

    related = []

    if category not in categories:
        return related

    keywords = categories[category]

    for q in questions:

        q_clean = preprocess(q)

        if current_question.lower() not in q.lower():

            for keyword in keywords:

                if keyword in q_clean:

                    related.append(q)

                    break

    return related[:4]


def get_faq_response(user_input, category=None):

    processed_questions = [
        preprocess(q)
        for q in questions
    ]

    processed_input = preprocess(user_input)

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        processed_questions + [processed_input]
    )

    similarity = cosine_similarity(
        vectors[-1],
        vectors[:-1]
    )

    best_match_index = similarity.argmax()

    best_score = similarity[0][best_match_index]

    if best_score > 0.15:

        matched_question = questions[best_match_index]

        answer = answers[best_match_index]

        related = get_related_questions(
            category,
            matched_question
        )

        return answer, related

    return (
        "Sorry, I couldn't fully understand your issue. "
        "Please try describing it differently."
    ), []


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/get")
def chatbot():

    global current_category

    user_input = request.args.get("msg")

    

    detected = detect_category(user_input)

    if detected:
        current_category = detected

    # GET RESPONSE

    answer, related = get_faq_response(
        user_input,
        current_category
    )


    related_html = ""

    if related:

        related_html += """
        <div class='related-title'>
            Related Issues
        </div>

        <div class='related-container'>
        """

        for item in related:

            related_html += f"""
            <button
                class='related-btn'
                onclick="sendRelated(`{item}`)"
            >
                {item}
            </button>
            """

        related_html += "</div>"

    final_response = f"""
    {answer}
    {related_html}
    """

    return jsonify(response=final_response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
