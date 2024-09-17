## About Resume Filter
Resume Filter is a web-based application built using the Django Framework to
help Human Resource teams. You simply upload a PDF resume or a collection of
PDF resumes in zip file format, and we extract valuable information for you.

## Environment Setup
These steps will help you run this project on your local machine.
### Prerequisites
- Make sure `Python 3.11` or above version installed on your system.
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
### Project Setup
- Clone this repository: [resume_filter](https://github.com/madhubabukencha/resume-filter) repo on your local machine.
- Change directory to the project root:
  ```
  cd resume-filter
  ```
- Install dependencies:
  ```
  pip install -r requirements.txt
  ```
### Google Authentication
This application uses Google authentication. So, create a `.env` file in
repository root directory with following variables.  Refer to the documentation
for detailed instructions: [Google Configuration Setup](https://github.com/madhubabukencha/django/blob/main/chap002-django-auth/google-config-setup.md) doc.
  ```
  CLIENT_ID=your_client_id
  GMAIL_SECRET=your_gmail_secret
  EMAIL_HOST_USER='your-gmail-id@gmail.com'
  EMAIL_HOST_PASSWORD='your_email_host_password'
  ```
### Database Setup
- Run the following commands to set up the database:
  ```shell
  $ python3 manage.py makemigrations
  $ python3 manage.py migrate
  ```
### Run the Application
- Start the development server
  ```
  python3 manage.py runserver
  ```
### Access the Application
- You can now access the application in your web browser at http://127.0.0.1:8000/.

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

