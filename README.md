# FisCal: Budget tracker calendar with fiscal analysis
[![Web App CI](https://github.com/software-students-fall2024/5-final-theonepiece/actions/workflows/CI.yml/badge.svg)](https://github.com/software-students-fall2024/4-containers-financiers/actions/workflows/web-app.yml)
## Description
FisCal is a budget-tracking calendar app that helps users manage their personal spending. Users can manually input expenses by adding events to a calendar, specifying the date, time, title (e.g., what they spent money on), and the amount spent. The app aggregates data to display daily, weekly, and monthly spending summaries and employs AI to analyze spending habits and provide personalized advice.

## Team Members
|Reyhan Abdul Quayum|Rashed Alneyadi|Sia Chen|Chloe Han|
|:--:|:--:|:--:|:--:|
|<a href='https://github.com/reyhanquayum'><img src='https://avatars.githubusercontent.com/u/115737572?v=4' width='40px'/></a>|<a href='https://github.com/brshood'><img src='https://avatars.githubusercontent.com/u/133962779?v=4' width='40px'/></a>|<a href='https://github.com/MambiChen'><img src='https://avatars.githubusercontent.com/u/122314736?v=4' width='40px'/></a>|<a href='https://github.com/jh7316'><img src='https://avatars.githubusercontent.com/u/95545960?s=88&v=4' width='40px'/></a>|


## Architecture

                +---------------------------+
                |      User's Browser       |
                +---------------------------+
                           |
                           v
                +---------------------------+
                |        Front-End          |
                |      (React/HTML/CSS)     |
                +---------------------------+
                           |
                           v
                +---------------------------+
                |        Back-End           |
                |      (Python/Flask)       |
                +---------------------------+
                           |
                           v
                +---------------------------+
                |     Docker Container      |
                |   (Front-End + Back-End)  |
                +---------------------------+
                           |
                           v
                +---------------------------+
                |   Docker Compose Setup    |
                |  (Coordinates Services)   |
                +---------------------------+
                           |
                           v
                +---------------------------+
                |  CI/CD Pipeline (GitHub)  |
                |       (Automated)         |
                +---------------------------+


## Folder Structure
```
- 5-FINAL-THEONEPIECE/
  - .github/
    - workflows/
      - event-logger.yml
    - note.txt
  - ux-design/
    - figma_wireframe.png
  - web-app/
    - __pycache__/
    - static/
    - templates/
      - Analytics.html
      - Base.html
      - Calendar.html
      - delete-acct.html
      - edit-user-info.html
      - index.html
      - Login.html
      - Menu.html
      - Search.html
      - Signup.html
    - user/
      - __init__.py
      - app.py
      - database.py
    - Dockerfile
    - Pipfile
    - Pipfile.lock
    - requirements.txt
    - test_app.py
  - .gitignore
  - docker-compose.yml
  - instructions.md
  - LICENSE
  - pyproject.toml
  - README.md
```



## Setup Instructions

### Prerequisites
* Docker Desktop

### Installation
1. Clone the repo:
```bash
git clone https://github.com/software-students-fall2024/5-final-theonepiece.git
cd 5-final-theonepiece
```
2. If using Docker Desktop application, start Docker Desktop if you haven't already
3. Build and start the containers with Docker Compose
```bash
docker-compose down
docker-compose build
docker-compose up
```

4. Access the Web App.

    You should be able to locally access web-app running on http://127.0.0.1:5000/

5. Sign up using by inputting your custom info and proceed to log in and use the app
  

## Thank you!