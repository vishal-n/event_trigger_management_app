**The app is deployed here:** https://event-trigger-management-app.onrender.com/docs <br>


<br>**Steps to run the application locally:**

**1.** Run the command: git clone git@github.com:vishal-n/event_trigger_management_app.git

**2.** Once the repo is installed, cd into the repository and run the command: **pip install -r requirements.txt**

**3.** Once all the requirements / dependencies are installed, run the command: **uvicorn app.main:app --reload**

**4.** The command mentioned in step 3, starts the localhost server

**5.** Once the locahost server has started running, visit this link to refer the API docs and also invoke the APIs: **http://127.0.0.1:8000/docs**

**6.** To run the app in a docker container, ensure docker is running in your machine and run this command: <br>
**docker-compose up --build**

**7.** After step 6 is successful, the link to the localhost should be visible here: http://0.0.0.0:8000/docs


**8.** Sample API request / response:
```bash
API: GET /triggers/scheduled/

Response:

{
  "scheduled_triggers": [
    {
      "id": 1,
      "name": "test1",
      "interval_minutes": 10,
      "fire_in_minutes": 10,
      "recurring": false,
      "created_at": "2025-02-02T14:34:58.415939"
    },
    {
      "id": 2,
      "name": "New schedule",
      "interval_minutes": 5,
      "fire_in_minutes": 5,
      "recurring": false,
      "created_at": "2025-02-02T16:00:19.716285"
    }
  ]
}
```

```bash
API: POST /triggers/scheduled/

Request Body:

{
  "name": "New schedule",
  "interval_minutes": 5,
  "fire_in_minutes": 5,
  "recurring": false
}

Response:

{
  "message": "Scheduled trigger created",
  "id": 2
}
```

```bash
API: PUT /triggers/scheduled/{trigger_id}

Request Body:

{
  "name": "test2",
  "interval_minutes": 10,
  "fire_in_minutes": 10,
  "recurring": false
}

Response:

{
  "message": "Scheduled trigger updated"
}
```

```bash
API: POST /triggers/scheduled/test/

Response:

{
  "message": "Test scheduled trigger will fire in 5 minutes."
}
```

```bash
API: POST /triggers/api/

Request Body:

{
  "name": "webhook auth api",
  "endpoint": "https://example.com/webhook",
  "payload": 
  {
    "user_id": 123,
    "action": "purchase"
  }
}

Response:

{
  "message": "API trigger created",
  "id": 1
}
```

```bash
API: GET /triggers/api/

Response:
{
  "api_triggers": 
  [
    {
      "id": 1,
      "name": "webhook auth api",
      "endpoint": "https://example.com/webhook",
      "payload": {
        "action": "purchase",
        "user_id": 123
      },
      "created_at": "2025-02-02T16:10:52.839818"
    }
  ]
}
```

```bash
API: GET /logs/

Response:

{
  "logs": [
    {
      "id": 1,
      "trigger_id": 2,
      "executed_at": "2025-02-02T16:05:19.826488",
      "is_test": false,
      "trigger_type": "scheduled",
      "is_archived": false
    }
  ]
}
```

```bash
API: GET /logs/?archived=true

Response:

{
  "logs": []
}
```