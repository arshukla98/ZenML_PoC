## Pre-requisites and Basic ZenML Commands

1. Python 3.7 or higher: Get it from here: https://www.python.org/downloads/
```
python --version # Mine is 3.11.0
```

2. Activate your Virtual Environment:
```
#create a virtual environment
python -m venv .venv
#Activate your virtual environmnent in your project folder
source .venv/Scripts/activate
```

3. See the python dependencies list

```
(.venv) $ pip list
Package    Version
---------- -------
pip        22.3
setuptools 65.5.0

[notice] A new release of pip available: 22.3 -> 24.2
[notice] To update, run: python.exe -m pip install --upgrade pip
```

4. Install Zenml

```
(.venv) $ pip install zenml
```

5. Check the list. Now you will notice more libraries.

```
(.venv) $ pip list
Package            Version
------------------ -----------
alembic            1.8.1
annotated-types    0.7.0
asttokens          2.4.1
bcrypt             4.0.1
certifi            2024.8.30
charset-normalizer 3.3.2
click              8.1.3
cloudpickle        2.2.1
colorama           0.4.6
comm               0.2.2
decorator          5.1.1
distro             1.9.0
docker             7.1.0
executing          2.1.0
gitdb              4.0.11
GitPython          3.1.43
greenlet           3.1.1
idna               3.10
ipython            8.28.0
ipywidgets         8.1.5
jedi               0.19.1
jupyterlab_widgets 3.0.13
Mako               1.3.5
markdown-it-py     3.0.0
MarkupSafe         2.1.5
matplotlib-inline  0.1.7
mdurl              0.1.2
packaging          24.1
parso              0.8.4
passlib            1.7.4
pip                22.3
prompt_toolkit     3.0.48
psutil             6.0.0
pure_eval          0.2.3
pydantic           2.8.2
pydantic_core      2.20.1
pydantic-settings  2.5.2
Pygments           2.18.0
PyMySQL            1.1.1
python-dateutil    2.9.0.post0
python-dotenv      1.0.1
pywin32            307
PyYAML             6.0.2
requests           2.32.3
rich               13.9.2
setuptools         65.5.0
six                1.16.0
smmap              5.0.1
SQLAlchemy         2.0.35
SQLAlchemy-Utils   0.41.2
sqlmodel           0.0.18
stack-data         0.6.3
traitlets          5.14.3
typing_extensions  4.12.2
urllib3            2.2.3
wcwidth            0.2.13
widgetsnbextension 4.0.13
zenml              0.67.0

[notice] A new release of pip available: 22.3 -> 24.2
[notice] To update, run: python.exe -m pip install --upgrade pip
```

6. To Launch zenml server and dashboard locally

```
pip install "zenml[server]"
```

7. See the zenml Version:

```
(.venv) $ zenml version

     ________                      __       __  __
    |        \                    |  \     /  \|  \
     \$$$$$$$$  ______   _______  | $$\   /  $$| $$
        /  $$  /      \ |       \ | $$$\ /  $$$| $$
       /  $$  |  $$$$$$\| $$$$$$$\| $$$$\  $$$$| $$
      /  $$   | $$    $$| $$  | $$| $$\$$ $$ $$| $$
     /  $$___ | $$$$$$$$| $$  | $$| $$ \$$$| $$| $$_____
    |  $$    \ \$$     \| $$  | $$| $$  \$ | $$| $$     \
     \$$$$$$$$  \$$$$$$$ \$$   \$$ \$$      \$$ \$$$$$$$$

version: 0.67.0
```

8. Initiate a new repository inside Project Root

```
(.venv) $ zenml init
Migrating the ZenML global configuration from version 0.65.0 to version 0.67.0...
⠋ Initializing ZenML repository at <Project Root>.
Backing up the database before migration.
Database successfully backed up to the 'C:\Users\<username>\AppData\Roaming\zenml\database_backup\zenml-backup.db' backup file. If something goes wrong with the upgrade, ZenML will attempt to restore the database from this backup automatically.
Successfully cleaned up database dump file C:\Users\<username>\AppData\Roaming\zenml\databa⠼ Initializing ZenML repository at <Project Root>.
Setting the repo active workspace to 'default'.
⠸ Initializing ZenML repository at <Project Root>.
ZenML repository initialized at <Project Root>
The local active stack was initialized to 'default'. This local configuration will only  
take effect when you're running ZenML from the initialized repository root, or from a    
subdirectory. For more information on repositories and configurations, please visit      
https://docs.zenml.io/user-guide/starter-guide/understand-stacks.
```

9. To run the dashboard locally in Windows:

```
(.venv) $ zenml up --blocking
The local ZenML dashboard is about to deploy in a blocking process. You can connect to itusing the 'default' username and an empty password.
Deploying a local ZenML server with name 'local'.
Migrating the ZenML global configuration from version 0.65.0 to version 0.67.0...
Starting ZenML Server as blocking process... press CTRL+C once to stop it.
INFO:     Started server process [10008]
INFO:     Waiting for application startup.
Not writing the global configuration to disk in a ZenML server environment.
Not writing the global configuration to disk in a ZenML server environment.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8237 (Press CTRL+C to quit)
```

## Integration of MLflow with ZenML

We are using mlflow as the experiment tracker, to track our model,artifacts, hyperparameter values. We are registering the stack component, experiment tracker, model-deployer here:

```
#Integrating mlflow with ZenML
zenml integration install mlflow -y

#Register the experiment tracker
zenml experiment-tracker register mlflow_tracker --flavor=mlflow

#Registering the model deployer
zenml model-deployer register mlflow_deployer --flavor=mlflow

#Registering the stack
zenml stack register mlflow_stack -a default -o default -d mlflow_deployer -e mlflow_tracker --set

#See Zenml Stacks
zenml stack list
```