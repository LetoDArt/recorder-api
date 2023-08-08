# Recorder API

This project has been created as backend part of a project written for final qualifying work in SFedU (Rostov-on-Don).
The goal of application to connect with client application via HTTP and WS channels for traffic sign recognition.


## Run application

### Preparations

Application needs to be properly set in order to run. The first step is to install all requirements 
from `requirements.txt` with command:

```commandline
    pip install -r requirements.txt 
```

after requirements, application works with environment variables, so in `app` module, 
there should be file `.env`. It must contain these variables:


```env
    SECRET_KEY="<here's secret key for tokens>"
    DATABASE_NAME=<database name>
    DATABASE_USER=<database user>
    DATABASE_PASSWORD=<user password>
    DATABASE_HOST=<host>
    DATABASE_PORT=<port>
```

After that step application could start, but it requires the prepared model of recognition, 
it should be placed to module `recogniter` in folder `assets` under the name `vgg16_deepstreet_training.h5`.

### Starting application

In order to start application locally, command:

```commandline
    python manage.py runserver
```

This command will start application only on local machine on 127.0.0.1:8000. 
If it needs to be done on local network with address of a machine in this network, then:

```commandline
    python manage.py runserver 0.0.0.0:8000
```