**Steps to run the application locally:**

**1.** Run the command: git clone git@github.com:vishal-n/event_trigger_management_app.git

**2.** Once the repo is installed, cd into the repository and run the command: **pip install -r requirements.txt**

**3.** Once all the requirements / dependencies are installed, run the command: **uvicorn app.main:app --reload**

**4.** The command mentioned in step 3, starts the localhost server

**5.** Once the locahost server has started running, visit this link to refer the API docs and also invoke the APIs: **http://127.0.0.1:8000/docs**

**6.** To run the app in s docker container, ensure docker is running in your machine and run this command: <br>
**docker-compose up --build**

**7.** The app is deployed here: https://event-trigger-management-app.onrender.com/docs
