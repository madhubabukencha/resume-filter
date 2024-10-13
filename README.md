## About Resume Filter
Searching for required skills in a large amount of resumes is a tedious task for HR teams. Resume Filter is a web-based application built using the Django framework to assist Human Resource teams. In the Resume Filter app, you simply upload PDF resumes, and we extract valuable information for you. Once your documents are processed, you can filter the required skills by using key terms like "Python," "Java," "Sales Manager," etc., and you can download the data in either "Excel" or "CSV" file formats.

## Environment Setup
These steps will help you to run this project on your local machine.
### Prerequisites
- Make sure have `Python 3.11` or above version installed on your system.
### Create Virtual Environment
- Create a virtual environment named resume-filter-venv using the following command:
  ```bash
  python3 -m venv resume-filter-venv
  ```
- Activate virtual environment on **MAC/Linux**
  ```bash
  source resume-filter-venv/bin/activate
  ```
- Activate virtual environment on **Window**
  ```
  resume-filter-venv\Scripts\activate
  ```
### Installing Dependencies
- Clone Repository: [resume-filter](https://github.com/madhubabukencha/resume-filter) repo on your local machine.
- Change directory to the project root:
  ```
  cd resume-filter
  ```
- Install dependencies:
  ```
  pip install -r requirements.txt
  ```
## Google Authentication
This application uses Google authentication. So, create a `.env` file in
repository root directory with following variables.  Refer to the documentation
for detailed instructions: [Google Configuration Setup](https://github.com/madhubabukencha/django/blob/main/chap002-django-auth/google-config-setup.md) doc.
  ```
  CLIENT_ID=your_client_id
  GMAIL_SECRET=your_gmail_secret
  EMAIL_HOST_USER='your-gmail-id@gmail.com'
  EMAIL_HOST_PASSWORD='your_email_host_password'
  ```
## Database Setup
- This project is using MySQL Database, so add below
  environment variables to your `.env` file. If you are using MySQL first time or 
  migrating from SQLite to MySQL refer migration document [here](https://github.com/madhubabukencha/django/tree/main/chap003-django-db/mysql-setup).
  ```
  DB_NAME="your_db_name"
  DB_USER="your_db_user_name"
  DB_PASSWORD="db_user_password"
  DB_HOST="localhost"
  DB_PORT="3306"
  ```
- Now login to MySQL Workbench with your MySQL username and password and create a new database. We are going to use it
to store our tables. Make sure database is empty to avoid migration issues.
  ```
  CREATE DATABASE your_database_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  ```
- Change directory to
  ```
  cd resume-filter/resume_filter
  ```
- Run the following commands to set up the database:
  ```shell
  $ python3 manage.py makemigrations
  $ python3 manage.py migrate
  ```
- If you want to access admin panel create super user
  ```shell
  $python3 manage.py createsuperuser
  ```
## OpenAI setup
- We are using OpenAI to generate various summaries from the extracted resume text. To make OpenAI work add below variable in your `.env` file
  ```
  OPENAI_API_KEY="your_open_api_key"
  ```
## Run the Application
- Start the development server
  ```
  python3 manage.py runserver
  ```
### Access the Application
- You can now access the application in your web browser at http://127.0.0.1:8000/.

### Sample Dataset
- Download sample resume dataset from kaggle [website](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset?resource=download)

## Troubleshooting
Here you can find solutions for possible errors
### dbshell error
If you face below error:
``` shell
PS D:\Projects\MCA-Project\resume-filter\resume_filter> python manage.py dbshell

CommandError: You appear not to have the 'sqlite3' program installed or on your path.
```
Download file like below one (sqlite-tools-win-x64-3460100.zip) from below url and unzip it. Copy and paste all files inside it in the place where manage.py exists:
https://www.sqlite.org/download.html

sqlite-tools-win-x64-3460100.zip: 
A bundle of command-line tools for managing SQLite database files, including the command-line shell program, the sqldiff.exe program, and the sqlite3_analyzer.exe program. 64-bit.

