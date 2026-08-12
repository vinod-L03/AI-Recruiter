me
🤖 AI Recruiter

An AI-powered recruitment system that helps recruiters analyze resumes, recommend suitable jobs, conduct multiple interview rounds, evaluate candidates, and determine employee eligibility.

🎯 Project Objective

The main goal of AI Recruiter is to reduce manual recruitment effort by automating the process from resume screening to final candidate selection.

✨ Features
📄 Resume Analysis
Upload candidate resumes in PDF format.
Automatically extract:
Candidate Name
Email
Phone Number
Location
Branch
Skills
Generate a Resume Score out of 100.
💼 Job Matching

The system compares the candidate's skills with job requirements and recommends suitable positions such as:

Software Engineer
Python Developer
Java Developer
Frontend Developer
Full Stack Developer
Backend Developer
AI/ML Engineer
Computer Vision Engineer
Data Analyst
Data Scientist
Database Developer
Cloud Engineer
DevOps Engineer
👨‍🎓 Student Login

Students can access the interview process using the email detected from their uploaded resume.

📝 Multi-Round Assessment

The recruitment process contains multiple rounds:

Aptitude Round
MCQ-based questions
Increasing difficulty
Coding Round
Programming and coding questions
Increasing difficulty
Communication Round
Evaluates communication ability
Technical Interview
Questions based on the candidate's resume
Questions based on the recommended job role
Evaluates technical knowledge
📊 Automatic Evaluation

The system calculates scores for the different assessment rounds and produces an overall interview result.

✅ Employee Eligibility

The current eligibility rule is:

Interview Score > 80
        ↓
    ELIGIBLE
Interview Score ≤ 80
        ↓
 NOT ELIGIBLE
📊 Recruiter Dashboard

The admin/recruiter dashboard displays:

Total Candidates
Average Resume Score
Interviews
Eligible Candidates
Not Eligible Candidates
Interview Pending
Recent Candidates
Recommended Jobs
Interview Results
🔄 Recruitment Workflow
Admin Login
     ↓
Upload Resume
     ↓
Resume Analysis
     ↓
Extract Candidate Details
     ↓
Resume Score
     ↓
Suitable Job Matching
     ↓
Student Login
     ↓
Aptitude Round
     ↓
Coding Round
     ↓
Communication Round
     ↓
Technical Interview
     ↓
Interview Score
     ↓
Eligibility Decision
     ↓
Eligible / Not Eligible
🛠️ Technologies Used
Python
Streamlit
PDFPlumber
PyPDF
Regular Expressions
Git
GitHub
📁 Project Structure
AI-Recruiter/
│
├── app.py
└── README.md
⚙️ Installation

Clone the repository:

git clone https://github.com/vinod-L03/AI-Recruiter.git

Go to the project directory:

cd AI-Recruiter

Install the required packages:

pip install streamlit pdfplumber pypdf
▶️ Run the Application
streamlit run app.py

The application will open in your browser.

👥 User Roles
👨‍💼 Admin / Recruiter

The recruiter can:

Upload resumes
Analyze candidates
View resume scores
View suitable jobs
Monitor interviews
View candidate results
Check eligibility
👨‍🎓 Student

The student can:

Log in using their resume email
Attend aptitude round
Attend coding round
Attend communication round
Attend technical interview
View their assessment result
🎯 Advantages
Saves recruiter time
Automates resume screening
Provides job recommendations
Reduces manual candidate evaluation
Supports multiple interview rounds
Provides centralized candidate information
Enables faster candidate selection
Provides consistent assessment rules
🚀 Future Enhancements
AI-powered answer evaluation using an LLM
Voice-based interviews
Facial/emotion analysis where appropriate and consented
Database integration
Email notifications
Resume ranking
Advanced coding evaluation
Recruiter reports and analytics
Cloud deployment
Authentication with secure password management
👨‍💻 Author
Bomma Vinod Kumar
Bomma Vinod Kumar

AI Recruiter — Resume Analysis • Job Matching • Multi-Round Interview • Employee Eligibility
