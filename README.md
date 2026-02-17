🫀 AI-Enabled Organ Donation and Transplant Matching System
📌 Overview

The AI-Enabled Organ Donation and Transplant Matching System is a web-based healthcare platform designed to automate and optimize the organ donor–recipient matching process using Machine Learning.

The system integrates AI-based intelligent matching, centralized database management, and real-time monitoring within a secure digital platform using Flask and XAMPP (MySQL).

🎯 Objectives

Automate organ donor–recipient matching using AI

Improve accuracy and fairness in organ allocation

Reduce manual coordination delays

Enable centralized medical record management

Provide transparency through dashboards and monitoring

🏗️ System Architecture

Frontend Layer – HTML, CSS, JavaScript

Backend Layer – Flask (Python)

Machine Learning Layer – Random Forest (Scikit-learn)

Database Layer – MySQL (XAMPP Server)

AI Assistance Layer – NLTK Chatbot

🔄 Workflow

Donors, Patients, Hospitals, OPO, NOTTO, and Admin log in using secure role-based authentication.

Donor and patient medical details are registered and stored in a centralized MySQL database hosted on XAMPP.

OPO verifies donor eligibility, Admin validates records, and NOTTO monitors compliance and allocation fairness.

The Random Forest algorithm analyzes medical parameters (blood group, tissue type, urgency, age, distance, medical history).

The system generates compatibility scores and ranks suitable donor–recipient pairs.

Hospitals review matches, confirm transplant decisions, and real-time notifications and dashboards ensure transparency.

🧠 Machine Learning Model

Algorithm Used: Random Forest (Scikit-learn)

Features:

Blood Group

Tissue Compatibility

Age

Medical Urgency

Geographic Distance

Patient Medical History

🛠️ Tech Stack
Component	Technology Used
Frontend	HTML, CSS, JavaScript
Backend	Python (Flask)
Machine Learning	Scikit-learn, Pandas
Database	MySQL (XAMPP Server)
Chatbot	NLTK
🚀 Installation & Setup (Using XAMPP)
1️⃣ Install XAMPP

Download and install XAMPP

Start Apache and MySQL from XAMPP Control Panel

2️⃣ Create Database

Open http://localhost/phpmyadmin

Create a new database (e.g., organ_matching_db)

Import the provided .sql file

3️⃣ Configure Flask App

Update database configuration in your config.py:

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_DB = 'organ_matching_db'

4️⃣ Install Dependencies
pip install -r requirements.txt

5️⃣ Run Application
python app.py


Open in browser:

http://127.0.0.1:5000/

👨‍💻 My Contribution

Data preprocessing and feature engineering

Model building using Random Forest

Backend development using Flask

MySQL database integration using XAMPP

Chatbot implementation using NLTK

Complete system deployment and testing
