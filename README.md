# PCR Dashboard Platform

This is the implementation of the dashboard system for the PCR project. The dashboard system is used to visualize the data (including the sent questions and the received reponse) from the deployments.

To deploy the system on your end, run `python manage.py runserver`

Currently, the dashboard system is also deployed on [Heroku](https://dashboard.heroku.com/apps), a cloud platform supporting Django applications. ~~Please follow the steps in the deploy panel to push and deploy your updates there.~~ The live dashboard app will be automatically updated if commits are pushed to the __main__ branch.

The live dashboard website is running at https://pcrdashboard.herokuapp.com/dataviewer/tracking/.