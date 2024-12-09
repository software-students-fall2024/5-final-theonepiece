# FisCal: Budget tracker calendar with fiscal analysis
[![CI/CD](https://github.com/software-students-fall2024/5-final-theonepiece/actions/workflows/CI-CD.yml/badge.svg)](https://github.com/software-students-fall2024/5-final-theonepiece/actions/workflows/CI-CD.yml)
## Description
FisCal is a budget-tracking calendar app with AI integration that helps users manage their personal spending. Users can manually input expenses by adding events to a calendar, specifying the date, time, title (e.g., what they spent money on), and the amount spent. The app aggregates data to display daily, weekly, and monthly spending summaries and employs AI to analyze spending habits and provide personalized advice.

## Deployment
The app is live and can be accessed at: [http://67.207.91.193:5000/](http://67.207.91.193:5000/)

## Docker Image
The image for the web-app subsystem is deployed on Docker hub on this [link](https://hub.docker.com/r/aesuran/theonepiece).

## Team Members
|Reyhan Abdul Quayum|Rashed Alneyadi|Sia Chen|Chloe Han|
|:--:|:--:|:--:|:--:|
|<a href='https://github.com/reyhanquayum'><img src='https://avatars.githubusercontent.com/u/115737572?v=4' width='40px'/></a>|<a href='https://github.com/brshood'><img src='https://avatars.githubusercontent.com/u/133962779?v=4' width='40px'/></a>|<a href='https://github.com/MambiChen'><img src='https://avatars.githubusercontent.com/u/122314736?v=4' width='40px'/></a>|<a href='https://github.com/jh7316'><img src='https://avatars.githubusercontent.com/u/95545960?s=88&v=4' width='40px'/></a>|

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
3. Add a .env file on the root directory, in the format shown in the example.env file and the actual contents  will be delivered to graders via discord
4. Build and start the containers with Docker Compose
```bash
docker-compose down
docker-compose build
docker-compose up
```

5. Access the Web App.

    You should be able to locally access web-app running on http://127.0.0.1:5000/

6. Sign up using by inputting your custom info and proceed to log in and use the app
  

## Thank you!
