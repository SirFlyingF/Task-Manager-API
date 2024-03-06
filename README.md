# Welcome to TaskMan

TaskMan is a task manager tool complete with a user authentication system

### Installation
clone the repository as follows:
```
git clone <url/.git>
```

Install dependencies
```
pip3 install -r requirements.txt
```

To run application you'll need a .env file in root directory next to config.py file. Set environment variable 'ENVIRON' as either 'PROD','TEST' or 'DEBUG. Set Appropriate params such as HOST PORT, DB_*, SECRET_KEY etc.

After environment vars are set, run the below file
```
source deploy.zsh
```
Note : Similar file could be written for docker but we'll keep it zsh for now.

Dynamic scaling is not supported and number of workers need to be added manually to deploy.zsh as needed

### API reference
For API reference see openapi.yaml

### Misc.
- Users when created have a position USER and can be changed to ADMIN. GetAllTasks transcation return all the the tasks in the DB if the user is ADMIN but will only show tasks created by the user if position is USER
- To change a USER to ADMIN, some kind of update needs to be run at the DB level. No application endpoint currently exists for it.
- Users' identity is established using email and password only.
- JWT token with a TTL of 30min is used. Users will have to sign back in after the token expired Refresh tokens are currently not supported
- Conflict case of email already existing for a SignUp transaction is handled at he app level because DBs such as SQLite do not support a Unique constraint on columns other than the primary key. Even though models are defines with this constrain at the ORM level

- Tasks have an attribute 'active_ind' which is used to soft delete. Reactivating tasks is currently not supported
- Duplicate tasks are allowed. Here Duplicate means a Task by the same user with same title.
- Filtering tasks is currently not supported
- Pagination works by taking 'page' and 'page_size' query params in GetAllTasks transaction.

- Config for TEST environment is currently hardcoded in config.py file for easy testing on local machine.
- While DEBUG config exist, logging is not currently supported. It can be added later on and turned on via DEBUG config
- TEST environment is set up to call a method that builds the database structure from scratch. Will not be called in PROD and DEBUG but will create new DB in TEST