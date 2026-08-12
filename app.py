import streamlit as st
import pdfplumber
from pypdf import PdfReader
import re
from datetime import datetime


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Recruiter",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "candidates": [],
    "admin_logged_in": False,
    "student_logged_in": False,
    "student_email": "",
    "student_index": None,

    "interview_candidate": None,
    "interview_job": None,
    "interview_round": None,

    "round_questions": [],
    "round_index": 0,
    "round_scores": [],

    "aptitude_completed": False,
    "coding_completed": False,
    "communication_completed": False,
    "technical_completed": False,

    "interview_total_scores": [],

    "last_uploaded_candidate": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #f5f7fb;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827, #1e293b);
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    .hero {
        padding: 30px;
        border-radius: 20px;
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: white;
        font-size: 36px;
        margin-bottom: 8px;
    }

    .hero p {
        color: #e0e7ff;
        font-size: 17px;
    }

    .section {
        font-size: 25px;
        font-weight: 800;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .candidate-card {
        padding: 22px;
        border-radius: 18px;
        background: white;
        border: 1px solid #e5e7eb;
        margin-bottom: 18px;
    }

    .question-card {
        padding: 25px;
        border-radius: 18px;
        background: #eef2ff;
        border: 1px solid #c7d2fe;
        margin: 20px 0;
    }

    .login-box {
        max-width: 600px;
        margin: auto;
        padding: 30px;
        background: white;
        border-radius: 20px;
        border: 1px solid #e5e7eb;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# JOB DATABASE
# ============================================================

JOB_ROLES = {
    "Software Engineer": [
        "Python",
        "Java",
        "SQL",
        "Data Structures",
        "Algorithms"
    ],

    "Python Developer": [
        "Python",
        "SQL",
        "Git",
        "Django",
        "Flask"
    ],

    "Java Developer": [
        "Java",
        "SQL",
        "Git",
        "Spring",
        "Spring Boot"
    ],

    "Frontend Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React"
    ],

    "Full Stack Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "SQL"
    ],

    "Backend Developer": [
        "Python",
        "Java",
        "SQL",
        "Node.js",
        "Git"
    ],

    "AI/ML Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "PyTorch",
        "TensorFlow"
    ],

    "Computer Vision Engineer": [
        "Python",
        "OpenCV",
        "Deep Learning",
        "PyTorch",
        "YOLO"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Excel",
        "Power BI",
        "Pandas"
    ],

    "Data Scientist": [
        "Python",
        "Pandas",
        "NumPy",
        "Machine Learning"
    ],

    "Database Developer": [
        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB"
    ],

    "Cloud Engineer": [
        "AWS",
        "Azure",
        "Linux",
        "Docker"
    ],

    "DevOps Engineer": [
        "Linux",
        "Git",
        "Docker",
        "Kubernetes",
        "AWS"
    ]
}


# ============================================================
# ALL SKILLS
# ============================================================

ALL_SKILLS = [
    "Python",
    "Java",
    "C++",
    "C",
    "C#",
    "SQL",
    "HTML",
    "CSS",
    "JavaScript",
    "TypeScript",
    "React",
    "Angular",
    "Vue",
    "Node.js",
    "Django",
    "Flask",
    "Spring",
    "Spring Boot",
    "Git",
    "GitHub",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Oracle",
    "AWS",
    "Azure",
    "Docker",
    "Kubernetes",
    "Linux",
    "Excel",
    "Power BI",
    "Tableau",
    "Pandas",
    "NumPy",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "OpenCV",
    "YOLO",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Data Science",
    "Data Structures",
    "Algorithms",
    "DBMS",
    "Operating Systems",
    "Computer Networks",
    "Cyber Security"
]


# ============================================================
# PDF EXTRACTION
# ============================================================

def extract_text(uploaded_file):

    text = ""

    try:
        uploaded_file.seek(0)

        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception:
        pass

    if not text.strip():

        try:
            uploaded_file.seek(0)

            reader = PdfReader(uploaded_file)

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        except Exception:
            pass

    return text.strip()


# ============================================================
# CLEAN TEXT
# ============================================================

def clean_line(line):

    line = line.replace("\u00a0", " ")

    line = re.sub(
        r"\s+",
        " ",
        line
    )

    return line.strip()


# ============================================================
# EMAIL EXTRACTION
# ============================================================

def extract_email(text):

    if not text:
        return "Not detected"

    # Normal email
    pattern = (
        r'(?i)\b'
        r'[A-Z0-9._%+-]+'
        r'@'
        r'[A-Z0-9.-]+'
        r'\.'
        r'[A-Z]{2,}'
        r'\b'
    )

    match = re.search(pattern, text)

    if match:
        return match.group(0).strip()

    # PDF sometimes adds spaces
    cleaned = re.sub(
        r'\s+',
        '',
        text
    )

    match = re.search(
        pattern,
        cleaned
    )

    if match:
        return match.group(0).strip()

    return "Not detected"


# ============================================================
# PHONE
# ============================================================

def extract_phone(text):

    patterns = [
        r'\+91[\s-]?[6-9]\d{9}',
        r'\b[6-9]\d{9}\b',
        r'\+91[\s-]?\d{10}'
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:
            return match.group(0)

    return "Not detected"


# ============================================================
# LOCATION
# ============================================================

def extract_location(text):

    patterns = [
        r'(?i)(?:location|address|city)\s*[:\-]\s*([^\n]+)',
        r'(?i)(?:location|address|city)\s+([A-Za-z ,]+)'
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            location = clean_line(
                match.group(1)
            )

            if location:
                return location

    cities = [
        "Hyderabad",
        "Vijayawada",
        "Visakhapatnam",
        "Vizag",
        "Guntur",
        "Kakinada",
        "Rajahmundry",
        "Tirupati",
        "Bengaluru",
        "Bangalore",
        "Chennai",
        "Mumbai",
        "Pune",
        "Delhi",
        "Kolkata",
        "Warangal",
        "Coimbatore",
        "Andhra Pradesh"
    ]

    lower_text = text.lower()

    for city in cities:

        if city.lower() in lower_text:
            return city

    return "Not detected"


# ============================================================
# NAME VALIDATION
# ============================================================

def valid_name(line):

    line = clean_line(line)

    if not line:
        return False

    if len(line) < 4 or len(line) > 50:
        return False

    if "@" in line:
        return False

    if re.search(r'\d', line):
        return False

    words = line.split()

    if len(words) < 2 or len(words) > 5:
        return False

    blocked = [
        "resume",
        "curriculum vitae",
        "objective",
        "summary",
        "profile",
        "education",
        "experience",
        "skills",
        "project",
        "projects",
        "certification",
        "contact",
        "phone",
        "email",
        "college",
        "university",
        "polytechnic",
        "institute",
        "engineering",
        "government",
        "governament",
        "computer science"
    ]

    lower = line.lower()

    for word in blocked:

        if word in lower:
            return False

    return bool(
        re.fullmatch(
            r"[A-Za-z][A-Za-z .'-]*",
            line
        )
    )


# ============================================================
# NAME
# ============================================================

def extract_name(text):

    lines = [
        clean_line(x)
        for x in text.splitlines()
        if clean_line(x)
    ]

    # Explicit name field
    for line in lines:

        match = re.match(
            r'(?i)^(name|candidate name|full name)\s*[:\-]\s*(.+)$',
            line
        )

        if match:

            name = clean_line(
                match.group(2)
            )

            if valid_name(name):
                return name

    # Find email line and check lines around it
    email_index = -1

    for i, line in enumerate(lines[:50]):

        if "@" in line:
            email_index = i
            break

    if email_index >= 0:

        start = max(
            0,
            email_index - 8
        )

        for i in range(
            start,
            email_index
        ):

            if valid_name(lines[i]):
                return lines[i]

    # First 20 lines
    for line in lines[:20]:

        if valid_name(line):
            return line

    return "Not detected"


# ============================================================
# BRANCH
# ============================================================

def extract_branch(text):

    lower = text.lower()

    branch_keywords = {
        "CSE": [
            "computer science",
            "computer science and engineering",
            "cse"
        ],

        "AIML": [
            "artificial intelligence and machine learning",
            "aiml"
        ],

        "IT": [
            "information technology"
        ],

        "ECE": [
            "electronics and communication",
            "ece"
        ],

        "EEE": [
            "electrical and electronics",
            "eee"
        ],

        "MECH": [
            "mechanical engineering"
        ],

        "CIVIL": [
            "civil engineering"
        ]
    }

    result = {}

    for branch, words in branch_keywords.items():

        result[branch] = sum(
            1
            for word in words
            if word in lower
        )

    best = max(
        result,
        key=result.get
    )

    if result[best] == 0:
        return "Not detected"

    return best


# ============================================================
# SKILLS
# ============================================================

def extract_skills(text):

    lower = text.lower()

    found = []

    for skill in sorted(
        ALL_SKILLS,
        key=len,
        reverse=True
    ):

        pattern = (
            r'(?<![A-Za-z])'
            + re.escape(skill.lower())
            + r'(?![A-Za-z])'
        )

        if re.search(
            pattern,
            lower
        ):

            if skill not in found:
                found.append(skill)

    return found


# ============================================================
# RESUME SCORE
# ============================================================

def resume_score(
    text,
    email,
    phone,
    skills
):

    score = 0

    if email != "Not detected":
        score += 15

    if phone != "Not detected":
        score += 15

    if len(skills) >= 15:
        score += 30

    elif len(skills) >= 10:
        score += 25

    elif len(skills) >= 5:
        score += 20

    elif len(skills) >= 1:
        score += 10

    words = len(text.split())

    if words >= 500:
        score += 15

    elif words >= 300:
        score += 12

    elif words >= 150:
        score += 8

    else:
        score += 5

    sections = [
        "education",
        "skills",
        "projects",
        "experience",
        "certifications"
    ]

    for section in sections:

        if section in text.lower():
            score += 5

    return min(
        score,
        100
    )


# ============================================================
# JOB MATCHING
# ============================================================

def match_jobs(skills):

    candidate_skills = {
        x.lower()
        for x in skills
    }

    jobs = []

    for job, required in JOB_ROLES.items():

        matched = [
            skill
            for skill in required
            if skill.lower() in candidate_skills
        ]

        missing = [
            skill
            for skill in required
            if skill.lower() not in candidate_skills
        ]

        score = round(
            len(matched)
            / len(required)
            * 100
        )

        if matched:

            jobs.append({
                "job": job,
                "score": score,
                "matched": matched,
                "missing": missing
            })

    jobs.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return jobs


# ============================================================
# APTITUDE QUESTIONS
# 10 MCQs - INCREASING DIFFICULTY
# ============================================================

APTITUDE_QUESTIONS = [

    {
        "question": "If 5 + 3 × 2 = ?",
        "options": [
            "16",
            "11",
            "13",
            "10"
        ],
        "answer": "11"
    },

    {
        "question": "A number is increased from 200 to 250. What is the percentage increase?",
        "options": [
            "20%",
            "25%",
            "30%",
            "15%"
        ],
        "answer": "25%"
    },

    {
        "question": "The average of 10, 20, 30, 40 and 50 is:",
        "options": [
            "25",
            "30",
            "35",
            "40"
        ],
        "answer": "30"
    },

    {
        "question": "A train travels 240 km in 4 hours. What is its average speed?",
        "options": [
            "50 km/h",
            "55 km/h",
            "60 km/h",
            "65 km/h"
        ],
        "answer": "60 km/h"
    },

    {
        "question": "If A:B = 3:5 and B:C = 10:7, then A:C is:",
        "options": [
            "3:7",
            "6:7",
            "7:6",
            "5:7"
        ],
        "answer": "6:7"
    },

    {
        "question": "A can complete a job in 12 days and B in 18 days. How many days will they take together?",
        "options": [
            "6.5 days",
            "7.2 days",
            "8 days",
            "9 days"
        ],
        "answer": "7.2 days"
    },

    {
        "question": "A shopkeeper gives 20% discount on an item marked ₹1500. What is the selling price?",
        "options": [
            "₹1100",
            "₹1150",
            "₹1200",
            "₹1250"
        ],
        "answer": "₹1200"
    },

    {
        "question": "A sum becomes ₹12,000 from ₹10,000 in 2 years at simple interest. What is the annual rate?",
        "options": [
            "8%",
            "10%",
            "12%",
            "15%"
        ],
        "answer": "10%"
    },

    {
        "question": "If the probability of an event is 0.35, what is the probability that it does not occur?",
        "options": [
            "0.55",
            "0.60",
            "0.65",
            "0.75"
        ],
        "answer": "0.65"
    },

    {
        "question": "A bag contains 5 red, 4 blue and 3 green balls. Two balls are drawn without replacement. What is the probability that both are red?",
        "options": [
            "5/33",
            "10/33",
            "5/22",
            "2/11"
        ],
        "answer": "5/33"
    }
]


# ============================================================
# CODING QUESTIONS
# ============================================================

CODING_QUESTIONS = [

    {
        "question": "Write a program to reverse a string.",
        "keywords": [
            "reverse",
            "string"
        ]
    },

    {
        "question": "Write a program to check whether a string is a palindrome.",
        "keywords": [
            "palindrome",
            "reverse"
        ]
    },

    {
        "question": "Write a program to find the largest element in an array without using the built-in max() function.",
        "keywords": [
            "array",
            "largest",
            "loop"
        ]
    },

    {
        "question": "Write a program to find duplicate elements in an array and explain its time complexity.",
        "keywords": [
            "duplicate",
            "array",
            "time complexity"
        ]
    },

    {
        "question": "Write a program to implement binary search on a sorted array and explain why its complexity is O(log n).",
        "keywords": [
            "binary search",
            "sorted",
            "log",
            "o(log"
        ]
    },

    {
        "question": "Given an array of integers, find the maximum subarray sum using an efficient algorithm.",
        "keywords": [
            "maximum subarray",
            "sum",
            "kadane"
        ]
    },

    {
        "question": "Design an algorithm to detect a cycle in a singly linked list and explain its space complexity.",
        "keywords": [
            "cycle",
            "linked list",
            "slow",
            "fast"
        ]
    },

    {
        "question": "Explain and implement a solution for finding the longest substring without repeating characters.",
        "keywords": [
            "longest substring",
            "sliding window",
            "hash"
        ]
    }
]


# ============================================================
# COMMUNICATION QUESTIONS
# ============================================================

COMMUNICATION_QUESTIONS = [

    "Tell us about yourself and explain why you are interested in this job.",

    "Describe a challenging situation you faced in a project and how you handled it.",

    "How do you manage your time when you have multiple tasks with the same deadline?",

    "How would you explain a technical concept to a person who has no technical background?",

    "Describe a situation where you worked successfully as part of a team."
]


# ============================================================
# TECHNICAL QUESTIONS
# BASED ON RESUME / JOB
# ============================================================

def generate_technical_questions(candidate, job):

    questions = []

    skills = candidate["skills"]

    # Resume skill questions
    for skill in skills[:5]:

        questions.append(
            {
                "question":
                    f"You mentioned {skill} in your resume. "
                    f"Explain what {skill} is, where you used it, "
                    f"and describe one practical example.",
                "keywords": [
                    skill.lower(),
                    "project",
                    "example"
                ]
            }
        )

    # Job-specific questions
    if job == "Software Engineer":

        questions.extend([
            {
                "question":
                    "Explain the difference between an array and a linked list.",
                "keywords":
                    ["array", "linked list"]
            },
            {
                "question":
                    "What is time complexity? Explain O(n), O(log n) and O(n²).",
                "keywords":
                    ["time complexity", "o(n)", "o(log", "o(n²"]
            },
            {
                "question":
                    "Explain the four main concepts of object-oriented programming.",
                "keywords":
                    ["encapsulation", "inheritance", "polymorphism", "abstraction"]
            }
        ])

    elif job == "Python Developer":

        questions.extend([
            {
                "question":
                    "Explain the difference between a list, tuple and set in Python.",
                "keywords":
                    ["list", "tuple", "set"]
            },
            {
                "question":
                    "What is a Python dictionary and how does it work?",
                "keywords":
                    ["dictionary", "key", "value"]
            }
        ])

    elif job == "Java Developer":

        questions.extend([
            {
                "question":
                    "Explain inheritance and polymorphism in Java.",
                "keywords":
                    ["inheritance", "polymorphism"]
            },
            {
                "question":
                    "What is the difference between == and equals() in Java?",
                "keywords":
                    ["==", "equals"]
            }
        ])

    elif job == "AI/ML Engineer":

        questions.extend([
            {
                "question":
                    "Explain the difference between supervised and unsupervised learning.",
                "keywords":
                    ["supervised", "unsupervised"]
            },
            {
                "question":
                    "What is overfitting and how can you reduce it?",
                "keywords":
                    ["overfitting", "regularization"]
            }
        ])

    elif job == "Computer Vision Engineer":

        questions.extend([
            {
                "question":
                    "What is image preprocessing and why is it important?",
                "keywords":
                    ["preprocessing", "image"]
            },
            {
                "question":
                    "Explain the basic idea behind object detection.",
                "keywords":
                    ["object detection", "bounding"]
            }
        ])

    elif job == "Frontend Developer":

        questions.extend([
            {
                "question":
                    "Explain the difference between HTML, CSS and JavaScript.",
                "keywords":
                    ["html", "css", "javascript"]
            },
            {
                "question":
                    "What is the DOM and how does JavaScript interact with it?",
                "keywords":
                    ["dom", "javascript"]
            }
        ])

    elif job == "Data Analyst":

        questions.extend([
            {
                "question":
                    "Explain the difference between WHERE and HAVING in SQL.",
                "keywords":
                    ["where", "having"]
            },
            {
                "question":
                    "What is data cleaning and why is it important?",
                "keywords":
                    ["data cleaning", "missing"]
            }
        ])

    return questions[:8]


# ============================================================
# CODING SCORE
# ============================================================

def evaluate_coding(answer, question):

    if not answer.strip():
        return 0

    answer_lower = answer.lower()

    keywords = question.get(
        "keywords",
        []
    )

    matched = 0

    for keyword in keywords:

        if keyword.lower() in answer_lower:
            matched += 1

    keyword_score = 0

    if keywords:

        keyword_score = (
            matched / len(keywords)
        ) * 60

    length_score = 0

    words = len(answer.split())

    if words >= 100:
        length_score = 25

    elif words >= 70:
        length_score = 20

    elif words >= 40:
        length_score = 15

    elif words >= 20:
        length_score = 8

    structure_score = 0

    if any(
        word in answer_lower
        for word in [
            "def ",
            "function",
            "for ",
            "while ",
            "return",
            "algorithm"
        ]
    ):
        structure_score += 15

    return min(
        round(
            keyword_score
            + length_score
            + structure_score
        ),
        100
    )


# ============================================================
# COMMUNICATION SCORE
# ============================================================

def evaluate_communication(answer):

    if not answer.strip():
        return 0

    words = len(
        answer.split()
    )

    score = 0

    if words >= 120:
        score += 40

    elif words >= 80:
        score += 32

    elif words >= 50:
        score += 25

    elif words >= 30:
        score += 18

    elif words >= 15:
        score += 10

    useful = [
        "because",
        "example",
        "experience",
        "project",
        "team",
        "problem",
        "solution",
        "result",
        "learned",
        "communication"
    ]

    for word in useful:

        if word in answer.lower():
            score += 5

    return min(
        score,
        100
    )


# ============================================================
# TECHNICAL SCORE
# ============================================================

def evaluate_technical(
    answer,
    question
):

    if not answer.strip():
        return 0

    answer_lower = answer.lower()

    keywords = question.get(
        "keywords",
        []
    )

    matched = sum(
        1
        for keyword in keywords
        if keyword.lower() in answer_lower
    )

    keyword_score = 0

    if keywords:

        keyword_score = (
            matched / len(keywords)
        ) * 70

    words = len(
        answer.split()
    )

    explanation_score = 0

    if words >= 100:
        explanation_score = 30

    elif words >= 70:
        explanation_score = 25

    elif words >= 40:
        explanation_score = 18

    elif words >= 20:
        explanation_score = 10

    return min(
        round(
            keyword_score
            + explanation_score
        ),
        100
    )


# ============================================================
# RESET ROUND
# ============================================================

def start_round(
    candidate_index,
    round_name,
    questions,
    job
):

    st.session_state.interview_candidate = candidate_index
    st.session_state.interview_round = round_name
    st.session_state.round_questions = questions
    st.session_state.round_index = 0
    st.session_state.round_scores = []
    st.session_state.interview_job = job


# ============================================================
# SAVE ROUND
# ============================================================

def save_round_score(
    candidate,
    round_name,
    scores
):

    average = round(
        sum(scores) / len(scores)
    ) if scores else 0

    if "round_scores" not in candidate:
        candidate["round_scores"] = {}

    candidate["round_scores"][round_name] = average

    return average


# ============================================================
# ADMIN LOGIN
# ============================================================

if not st.session_state.admin_logged_in and not st.session_state.student_logged_in:

    st.markdown(
        """
        <div class="hero">
            <h1>🤖 AI Recruiter</h1>
            <p>AI-powered recruitment and interview platform</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    login_type = st.radio(
        "Login as",
        [
            "Recruiter / Admin",
            "Student"
        ],
        horizontal=True
    )

    st.divider()

    if login_type == "Recruiter / Admin":

        st.subheader(
            "🔐 Recruiter Login"
        )

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Login as Recruiter",
            type="primary",
            use_container_width=True
        ):

            if (
                username == "admin"
                and password == "admin123"
            ):

                st.session_state.admin_logged_in = True
                st.rerun()

            else:

                st.error(
                    "Invalid username or password."
                )

        st.info(
            "Demo login: admin / admin123"
        )

    else:

        st.subheader(
            "🎓 Student Login"
        )

        student_email = st.text_input(
            "Enter the email used in your resume",
            placeholder="example@gmail.com"
        ).strip().lower()

        if st.button(
            "Login as Student",
            type="primary",
            use_container_width=True
        ):

            found_index = None

            for index, candidate in enumerate(
                st.session_state.candidates
            ):

                candidate_email = candidate.get(
                    "email",
                    ""
                ).strip().lower()

                if (
                    candidate_email != "not detected"
                    and candidate_email == student_email
                ):

                    found_index = index
                    break

            if found_index is not None:

                st.session_state.student_logged_in = True
                st.session_state.student_email = student_email
                st.session_state.student_index = found_index

                st.success(
                    "Login successful."
                )

                st.rerun()

            else:

                st.error(
                    "No analyzed resume found for this email. "
                    "Please ask the recruiter to upload your resume first."
                )


# ============================================================
# ADMIN APPLICATION
# ============================================================

elif st.session_state.admin_logged_in:

    with st.sidebar:

        st.title(
            "🤖 AI Recruiter"
        )

        st.caption(
            "RECRUITER PANEL"
        )

        page = st.radio(
            "MENU",
            [
                "📊 Dashboard",
                "📄 Resume Analyzer",
                "👥 Candidates",
                "📈 Results"
            ]
        )

        st.divider()

        st.subheader(
            "Eligibility Rule"
        )

        st.success(
            "Interview Score > 80"
        )

        if st.button(
            "Logout"
        ):

            st.session_state.admin_logged_in = False
            st.rerun()


    # ========================================================
    # ADMIN DASHBOARD
    # ========================================================

    if page == "📊 Dashboard":

        st.markdown(
            """
            <div class="hero">
                <h1>Good Morning, Recruiter 👋</h1>
                <p>
                Find the right talent faster with AI-powered
                resume screening, job matching and interviews.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        candidates = st.session_state.candidates

        total = len(candidates)

        interviews = sum(
            1
            for c in candidates
            if c.get(
                "interview_completed",
                False
            )
        )

        eligible = sum(
            1
            for c in candidates
            if c.get(
                "status"
            ) == "Eligible"
        )

        not_eligible = sum(
            1
            for c in candidates
            if c.get(
                "status"
            ) == "Not Eligible"
        )

        pending = sum(
            1
            for c in candidates
            if c.get(
                "status"
            ) == "Interview Pending"
        )

        if total:

            average_resume = round(
                sum(
                    c["resume_score"]
                    for c in candidates
                ) / total
            )

        else:

            average_resume = 0

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric(
            "👥 Total Candidates",
            total
        )

        c2.metric(
            "📄 Avg Resume Score",
            f"{average_resume}/100"
        )

        c3.metric(
            "🎤 Interviews",
            interviews
        )

        c4.metric(
            "🟢 Eligible",
            eligible
        )

        c5.metric(
            "🔴 Not Eligible",
            not_eligible
        )

        st.markdown(
            '<div class="section">📋 Recruitment Pipeline</div>',
            unsafe_allow_html=True
        )

        p1, p2, p3 = st.columns(3)

        p1.info(
            f"🟡 Interview Pending\n\n### {pending}"
        )

        p2.success(
            f"🟢 Eligible\n\n### {eligible}"
        )

        p3.error(
            f"🔴 Not Eligible\n\n### {not_eligible}"
        )

        st.markdown(
            '<div class="section">👥 Recent Candidates</div>',
            unsafe_allow_html=True
        )

        if not candidates:

            st.info(
                "No candidates yet. Upload a resume."
            )

        else:

            for candidate in reversed(
                candidates[-10:]
            ):

                with st.container(border=True):

                    st.subheader(
                        f"👤 {candidate['name']}"
                    )

                    st.write(
                        f"📧 {candidate['email']}"
                    )

                    st.write(
                        f"📱 {candidate['phone']}"
                    )

                    st.write(
                        f"📍 {candidate['location']}"
                    )

                    r1, r2, r3 = st.columns(3)

                    r1.metric(
                        "Resume",
                        f"{candidate['resume_score']}/100"
                    )

                    interview_score = candidate.get(
                        "interview_score"
                    )

                    r2.metric(
                        "Interview",
                        "Pending"
                        if interview_score is None
                        else f"{interview_score}/100"
                    )

                    r3.metric(
                        "Status",
                        candidate["status"]
                    )


    # ========================================================
    # RESUME ANALYZER
    # ========================================================

    elif page == "📄 Resume Analyzer":

        st.title(
            "📄 Resume Analyzer"
        )

        st.write(
            "Recruiter uploads and analyzes the student's resume."
        )

        uploaded_file = st.file_uploader(
            "Upload Resume PDF",
            type=["pdf"]
        )

        if uploaded_file:

            st.success(
                f"Selected: {uploaded_file.name}"
            )

            if st.button(
                "🔍 Analyze Resume",
                type="primary",
                use_container_width=True
            ):

                with st.spinner(
                    "Analyzing resume..."
                ):

                    text = extract_text(
                        uploaded_file
                    )

                    if not text:

                        st.error(
                            "Could not extract text from this PDF."
                        )

                        st.stop()

                    name = extract_name(text)

                    email = extract_email(text)

                    phone = extract_phone(text)

                    location = extract_location(text)

                    branch = extract_branch(text)

                    skills = extract_skills(text)

                    score = resume_score(
                        text,
                        email,
                        phone,
                        skills
                    )

                    jobs = match_jobs(
                        skills
                    )

                    # Check existing candidate by email
                    existing_index = None

                    if email != "Not detected":

                        for i, old_candidate in enumerate(
                            st.session_state.candidates
                        ):

                            if old_candidate.get(
                                "email",
                                ""
                            ).lower() == email.lower():

                                existing_index = i
                                break

                    candidate = {
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "location": location,
                        "branch": branch,
                        "skills": skills,
                        "resume_score": score,
                        "jobs": jobs,
                        "resume_text": text,
                        "status": "Interview Pending",
                        "interview_completed": False,
                        "interview_score": None,
                        "question_scores": [],
                        "round_scores": {},
                        "created_at":
                            datetime.now().strftime(
                                "%d-%m-%Y %H:%M"
                            )
                    }

                    if existing_index is not None:

                        # Keep interview data
                        old = st.session_state.candidates[
                            existing_index
                        ]

                        candidate["interview_completed"] = old.get(
                            "interview_completed",
                            False
                        )

                        candidate["interview_score"] = old.get(
                            "interview_score"
                        )

                        candidate["status"] = old.get(
                            "status",
                            "Interview Pending"
                        )

                        candidate["round_scores"] = old.get(
                            "round_scores",
                            {}
                        )

                        candidate["question_scores"] = old.get(
                            "question_scores",
                            []
                        )

                        st.session_state.candidates[
                            existing_index
                        ] = candidate

                        saved_index = existing_index

                    else:

                        st.session_state.candidates.append(
                            candidate
                        )

                        saved_index = (
                            len(
                                st.session_state.candidates
                            ) - 1
                        )

                    st.session_state.last_uploaded_candidate = saved_index

                st.success(
                    "✅ Resume successfully analyzed and saved."
                )

        # ----------------------------------------------------
        # DISPLAY LAST CANDIDATE
        # ----------------------------------------------------

        if (
            st.session_state.last_uploaded_candidate
            is not None
        ):

            index = st.session_state.last_uploaded_candidate

            candidate = st.session_state.candidates[
                index
            ]

            st.divider()

            st.subheader(
                "👤 Candidate Information"
            )

            a1, a2 = st.columns(2)

            with a1:

                st.write(
                    f"**Name:** {candidate['name']}"
                )

                st.write(
                    f"**Email:** {candidate['email']}"
                )

                st.write(
                    f"**Phone:** {candidate['phone']}"
                )

            with a2:

                st.write(
                    f"**Location:** {candidate['location']}"
                )

                st.write(
                    f"**Branch:** {candidate['branch']}"
                )

                st.write(
                    f"**Status:** {candidate['status']}"
                )

            if candidate["email"] == "Not detected":

                st.error(
                    "⚠️ Email could not be detected. "
                    "Student login cannot be linked until the resume contains a readable email address."
                )

            else:

                st.success(
                    f"Student login email: {candidate['email']}"
                )

            s1, s2, s3 = st.columns(3)

            s1.metric(
                "📄 Resume Score",
                f"{candidate['resume_score']}/100"
            )

            s2.metric(
                "🛠 Skills Found",
                len(candidate["skills"])
            )

            s3.metric(
                "💼 Best Job",
                candidate["jobs"][0]["job"]
                if candidate["jobs"]
                else "None"
            )

            st.subheader(
                "🛠 Skills Found"
            )

            st.write(
                ", ".join(
                    candidate["skills"]
                )
                if candidate["skills"]
                else "No skills detected"
            )

            st.subheader(
                "💼 Suitable Jobs"
            )

            for number, job in enumerate(
                candidate["jobs"][:5],
                start=1
            ):

                with st.container(
                    border=True
                ):

                    j1, j2 = st.columns(
                        [5, 1]
                    )

                    j1.subheader(
                        f"{number}. {job['job']}"
                    )

                    j2.metric(
                        "Match",
                        f"{job['score']}%"
                    )

                    st.write(
                        "**Matching Skills:** "
                        + (
                            ", ".join(
                                job["matched"]
                            )
                            if job["matched"]
                            else "None"
                        )
                    )

                    st.write(
                        "**Skills to Improve:** "
                        + (
                            ", ".join(
                                job["missing"]
                            )
                            if job["missing"]
                            else "None"
                        )
                    )


    # ========================================================
    # CANDIDATES
    # ========================================================

    elif page == "👥 Candidates":

        st.title(
            "👥 Candidates"
        )

        search = st.text_input(
            "🔎 Search by name, email or skill"
        )

        if not st.session_state.candidates:

            st.info(
                "No candidates available."
            )

        for index, candidate in enumerate(
            st.session_state.candidates
        ):

            searchable = (
                candidate["name"]
                + " "
                + candidate["email"]
                + " "
                + " ".join(
                    candidate["skills"]
                )
            ).lower()

            if (
                search
                and search.lower()
                not in searchable
            ):
                continue

            with st.container(
                border=True
            ):

                st.subheader(
                    f"👤 {candidate['name']}"
                )

                st.write(
                    f"📧 {candidate['email']}"
                )

                st.write(
                    f"📱 {candidate['phone']}"
                )

                st.write(
                    f"📍 {candidate['location']}"
                )

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "Resume",
                    f"{candidate['resume_score']}/100"
                )

                score = candidate.get(
                    "interview_score"
                )

                c2.metric(
                    "Interview",
                    "Pending"
                    if score is None
                    else f"{score}/100"
                )

                c3.metric(
                    "Status",
                    candidate["status"]
                )


    # ========================================================
    # RESULTS
    # ========================================================

    elif page == "📈 Results":

        st.title(
            "📈 Interview Results"
        )

        completed = [
            c
            for c in st.session_state.candidates
            if c.get(
                "interview_completed",
                False
            )
        ]

        if not completed:

            st.info(
                "No completed interviews yet."
            )

        for candidate in completed:

            with st.container(
                border=True
            ):

                st.subheader(
                    f"👤 {candidate['name']}"
                )

                st.write(
                    f"📧 {candidate['email']}"
                )

                st.write(
                    f"💼 {candidate['jobs'][0]['job']}"
                    if candidate["jobs"]
                    else "No job"
                )

                r1, r2, r3 = st.columns(3)

                r1.metric(
                    "Resume",
                    f"{candidate['resume_score']}/100"
                )

                r2.metric(
                    "Interview",
                    f"{candidate['interview_score']}/100"
                )

                r3.metric(
                    "Status",
                    candidate["status"]
                )

                st.write(
                    "**Round Scores**"
                )

                for round_name, round_score in candidate.get(
                    "round_scores",
                    {}
                ).items():

                    st.write(
                        f"{round_name}: {round_score}/100"
                    )

                if candidate["status"] == "Eligible":

                    st.success(
                        "🟢 Candidate is ELIGIBLE"
                    )

                else:

                    st.error(
                        "🔴 Candidate is NOT ELIGIBLE"
                    )


# ============================================================
# STUDENT APPLICATION
# ============================================================

elif st.session_state.student_logged_in:

    index = st.session_state.student_index

    if (
        index is None
        or index >= len(
            st.session_state.candidates
        )
    ):

        st.error(
            "Student record not found."
        )

        st.session_state.student_logged_in = False
        st.rerun()

    candidate = st.session_state.candidates[index]

    with st.sidebar:

        st.title(
            "🎓 Student Portal"
        )

        st.write(
            f"👤 {candidate['name']}"
        )

        st.write(
            f"📧 {candidate['email']}"
        )

        st.divider()

        student_page = st.radio(
            "MENU",
            [
                "🏠 My Profile",
                "📝 Interview"
            ]
        )

        if st.button(
            "Logout"
        ):

            st.session_state.student_logged_in = False
            st.session_state.student_index = None
            st.session_state.student_email = ""
            st.rerun()


    # ========================================================
    # STUDENT PROFILE
    # ========================================================

    if student_page == "🏠 My Profile":

        st.markdown(
            f"""
            <div class="hero">
                <h1>Welcome, {candidate['name']} 👋</h1>
                <p>Your AI recruitment profile</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        a1, a2, a3 = st.columns(3)

        a1.metric(
            "📄 Resume Score",
            f"{candidate['resume_score']}/100"
        )

        a2.metric(
            "🛠 Skills",
            len(candidate["skills"])
        )

        a3.metric(
            "📋 Status",
            candidate["status"]
        )

        st.subheader(
            "👤 My Information"
        )

        st.write(
            f"**Name:** {candidate['name']}"
        )

        st.write(
            f"**Email:** {candidate['email']}"
        )

        st.write(
            f"**Phone:** {candidate['phone']}"
        )

        st.write(
            f"**Location:** {candidate['location']}"
        )

        st.write(
            f"**Branch:** {candidate['branch']}"
        )

        st.subheader(
            "🛠 My Skills"
        )

        st.write(
            ", ".join(
                candidate["skills"]
            )
        )

        st.subheader(
            "💼 Suitable Jobs"
        )

        for job in candidate["jobs"][:5]:

            with st.container(
                border=True
            ):

                st.write(
                    f"### {job['job']}"
                )

                st.write(
                    f"Match: {job['score']}%"
                )

                st.write(
                    "Matching Skills: "
                    + ", ".join(
                        job["matched"]
                    )
                )

        if candidate.get(
            "interview_score"
        ) is not None:

            st.divider()

            st.subheader(
                "🎯 Interview Result"
            )

            st.metric(
                "Final Interview Score",
                f"{candidate['interview_score']}/100"
            )

            if candidate["status"] == "Eligible":

                st.success(
                    "🟢 You are ELIGIBLE for the recommended job."
                )

            else:

                st.error(
                    "🔴 You are NOT ELIGIBLE."
                )


    # ========================================================
    # STUDENT INTERVIEW
    # ========================================================

    elif student_page == "📝 Interview":

        st.title(
            "📝 AI Interview"
        )

        # ----------------------------------------------------
        # IF NO ROUND STARTED
        # ----------------------------------------------------

        if st.session_state.interview_candidate is None:

            st.info(
                "Complete all rounds in order."
            )

            st.subheader(
                "Interview Process"
            )

            st.write(
                "1️⃣ Aptitude — 10 MCQs"
            )

            st.write(
                "2️⃣ Coding — Increasing difficulty"
            )

            st.write(
                "3️⃣ Communication"
            )

            st.write(
                "4️⃣ Technical — Resume based"
            )

            st.divider()

            st.subheader(
                "Round Status"
            )

            st.write(
                "🧠 Aptitude: "
                + (
                    "Completed"
                    if st.session_state.aptitude_completed
                    else "Pending"
                )
            )

            st.write(
                "💻 Coding: "
                + (
                    "Completed"
                    if st.session_state.coding_completed
                    else "Pending"
                )
            )

            st.write(
                "🗣️ Communication: "
                + (
                    "Completed"
                    if st.session_state.communication_completed
                    else "Pending"
                )
            )

            st.write(
                "🛠️ Technical: "
                + (
                    "Completed"
                    if st.session_state.technical_completed
                    else "Pending"
                )
            )

            st.divider()

            best_job = (
                candidate["jobs"][0]["job"]
                if candidate["jobs"]
                else "Software Engineer"
            )

            # Aptitude
            if not st.session_state.aptitude_completed:

                if st.button(
                    "🧠 Start Aptitude Round",
                    type="primary",
                    use_container_width=True
                ):

                    start_round(
                        index,
                        "Aptitude",
                        APTITUDE_QUESTIONS,
                        best_job
                    )

                    st.rerun()

            # Coding
            elif not st.session_state.coding_completed:

                if st.button(
                    "💻 Start Coding Round",
                    type="primary",
                    use_container_width=True
                ):

                    start_round(
                        index,
                        "Coding",
                        CODING_QUESTIONS,
                        best_job
                    )

                    st.rerun()

            # Communication
            elif not st.session_state.communication_completed:

                if st.button(
                    "🗣️ Start Communication Round",
                    type="primary",
                    use_container_width=True
                ):

                    questions = [
                        {
                            "question": q,
                            "keywords": [
                                "example",
                                "experience",
                                "situation"
                            ]
                        }
                        for q in COMMUNICATION_QUESTIONS
                    ]

                    start_round(
                        index,
                        "Communication",
                        questions,
                        best_job
                    )

                    st.rerun()

            # Technical
            elif not st.session_state.technical_completed:

                technical_questions = generate_technical_questions(
                    candidate,
                    best_job
                )

                if st.button(
                    "🛠️ Start Technical Round",
                    type="primary",
                    use_container_width=True
                ):

                    start_round(
                        index,
                        "Technical",
                        technical_questions,
                        best_job
                    )

                    st.rerun()

            else:

                st.success(
                    "🎉 All interview rounds completed!"
                )

                if candidate.get(
                    "interview_score"
                ) is not None:

                    st.metric(
                        "Final Interview Score",
                        f"{candidate['interview_score']}/100"
                    )

                    if candidate["status"] == "Eligible":

                        st.success(
                            "🟢 ELIGIBLE"
                        )

                    else:

                        st.error(
                            "🔴 NOT ELIGIBLE"
                        )


        # ----------------------------------------------------
        # ACTIVE ROUND
        # ----------------------------------------------------

        else:

            round_name = st.session_state.interview_round

            questions = st.session_state.round_questions

            q_index = st.session_state.round_index

            job = st.session_state.interview_job

            st.write(
                f"**Candidate:** {candidate['name']}"
            )

            st.write(
                f"**Job:** {job}"
            )

            st.write(
                f"**Round:** {round_name}"
            )

            st.progress(
                (
                    q_index
                    / len(questions)
                )
            )

            question_data = questions[
                q_index
            ]

            st.markdown(
                f"""
                <div class="question-card">
                    <h3>
                    Question {q_index + 1}
                    of {len(questions)}
                    </h3>
                    <p style="font-size:18px;">
                    {question_data['question']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # =================================================
            # APTITUDE MCQ
            # =================================================

            if round_name == "Aptitude":

                selected = st.radio(
                    "Select your answer:",
                    question_data["options"],
                    key=f"apt_{q_index}"
                )

                if st.button(
                    "Submit Answer →",
                    type="primary",
                    use_container_width=True
                ):

                    if (
                        selected
                        == question_data["answer"]
                    ):

                        score = 100

                    else:

                        score = 0

                    st.session_state.round_scores.append(
                        score
                    )

                    if (
                        q_index + 1
                        < len(questions)
                    ):

                        st.session_state.round_index += 1

                        st.rerun()

                    else:

                        average = save_round_score(
                            candidate,
                            "Aptitude",
                            st.session_state.round_scores
                        )

                        st.session_state.aptitude_completed = True

                        st.session_state.interview_candidate = None

                        st.session_state.round_questions = []

                        st.session_state.round_index = 0

                        st.session_state.round_scores = []

                        st.success(
                            f"Aptitude completed. Score: {average}/100"
                        )

                        st.rerun()

            # =================================================
            # CODING
            # =================================================

            elif round_name == "Coding":

                answer = st.text_area(
                    "Write your solution / explanation:",
                    height=250,
                    key=f"coding_{q_index}"
                )

                if st.button(
                    "Submit Coding Answer →",
                    type="primary",
                    use_container_width=True
                ):

                    if not answer.strip():

                        st.warning(
                            "Please provide your answer."
                        )

                    else:

                        score = evaluate_coding(
                            answer,
                            question_data
                        )

                        st.session_state.round_scores.append(
                            score
                        )

                        if (
                            q_index + 1
                            < len(questions)
                        ):

                            st.session_state.round_index += 1

                            st.rerun()

                        else:

                            average = save_round_score(
                                candidate,
                                "Coding",
                                st.session_state.round_scores
                            )

                            st.session_state.coding_completed = True

                            st.session_state.interview_candidate = None

                            st.session_state.round_questions = []

                            st.session_state.round_index = 0

                            st.session_state.round_scores = []

                            st.success(
                                f"Coding completed. Score: {average}/100"
                            )

                            st.rerun()

            # =================================================
            # COMMUNICATION
            # =================================================

            elif round_name == "Communication":

                answer = st.text_area(
                    "Your answer:",
                    height=220,
                    key=f"communication_{q_index}"
                )

                if st.button(
                    "Submit Answer →",
                    type="primary",
                    use_container_width=True
                ):

                    if not answer.strip():

                        st.warning(
                            "Please provide an answer."
                        )

                    else:

                        score = evaluate_communication(
                            answer
                        )

                        st.session_state.round_scores.append(
                            score
                        )

                        if (
                            q_index + 1
                            < len(questions)
                        ):

                            st.session_state.round_index += 1

                            st.rerun()

                        else:

                            average = save_round_score(
                                candidate,
                                "Communication",
                                st.session_state.round_scores
                            )

                            st.session_state.communication_completed = True

                            st.session_state.interview_candidate = None

                            st.session_state.round_questions = []

                            st.session_state.round_index = 0

                            st.session_state.round_scores = []

                            st.success(
                                f"Communication completed. Score: {average}/100"
                            )

                            st.rerun()

            # =================================================
            # TECHNICAL
            # =================================================

            elif round_name == "Technical":

                answer = st.text_area(
                    "Your technical answer:",
                    height=250,
                    key=f"technical_{q_index}"
                )

                if st.button(
                    "Submit Technical Answer →",
                    type="primary",
                    use_container_width=True
                ):

                    if not answer.strip():

                        st.warning(
                            "Please provide your answer."
                        )

                    else:

                        score = evaluate_technical(
                            answer,
                            question_data
                        )

                        st.session_state.round_scores.append(
                            score
                        )

                        if (
                            q_index + 1
                            < len(questions)
                        ):

                            st.session_state.round_index += 1

                            st.rerun()

                        else:

                            technical_average = save_round_score(
                                candidate,
                                "Technical",
                                st.session_state.round_scores
                            )

                            st.session_state.technical_completed = True

                            # --------------------------------
                            # FINAL SCORE
                            # --------------------------------

                            round_scores = candidate.get(
                                "round_scores",
                                {}
                            )

                            all_scores = [
                                round_scores.get(
                                    "Aptitude",
                                    0
                                ),
                                round_scores.get(
                                    "Coding",
                                    0
                                ),
                                round_scores.get(
                                    "Communication",
                                    0
                                ),
                                technical_average
                            ]

                            final_score = round(
                                sum(all_scores)
                                / len(all_scores)
                            )

                            candidate["interview_score"] = final_score

                            candidate["interview_completed"] = True

                            candidate["question_scores"] = all_scores

                            # EXACT RULE
                            if final_score > 80:

                                candidate["status"] = (
                                    "Eligible"
                                )

                            else:

                                candidate["status"] = (
                                    "Not Eligible"
                                )

                            # Reset active round
                            st.session_state.interview_candidate = None

                            st.session_state.round_questions = []

                            st.session_state.round_index = 0

                            st.session_state.round_scores = []

                            st.success(
                                f"Technical Round completed. Score: {technical_average}/100"
                            )

                            st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🤖 AI Recruiter • Resume Analysis • "
    "Job Matching • Aptitude • Coding • "
    "Communication • Technical Interview • "
    "Employee Eligibility"
)