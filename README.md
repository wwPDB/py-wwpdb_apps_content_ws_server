# py-wwpdb_apps_content_ws_server
OneDep Content Service

This package provides API end points for 
access to data stored in the OneDep database
and content with the mmCIF model files.

## Components

This package comprises a server front end and a consumer backend

## Installation

### Requirements

Communication between the front end and back end is via a RabbitMQ server
set by the variable SITE_RBMQ_SERVER_HOST in site-config

The front end and back end must share the same filesystem
They require SITE_WEB_APPS_TOP_SESSIONS_PATH to be set in OneDep site-config
The consumer requires access to the OneDep database and archive folder.

### server

pip install wwpdb.apps.content-ws-server[server]

### consumer

pip install wwpdb.apps.content-ws-server


## Running

### Server

WSGI scripts are provided for both use with an apache or Gunicorn

####Apache

WSGIScriptAlias /service/contentws wwpdb/apps/content_ws_server/webapp/doServiceRequest.wsgi

or

WSGIScriptAlias /service/contentws ${SITE_WEB_APPS_TOP_PATH}/wsgi/doServiceRequest_content.wsgi

####Gunicorn 

To run localhost with port 10005

pip install gunicorn
gunicorn wwpdb.apps.content_ws_server.webapp.wsgi --bind 0.0.0.0:10005

### Consumer

The following command runs a single consumer as a detached process

python -m wwpdb.apps.content_ws_server.service.ContentRequestServiceHandler --start

or for more options

python -m wwpdb.apps.content_ws_server.service.ContentRequestServiceHandler --help

## Configuring new API calls

Definitions are stored in a JSON file in wwpdb.apps.content_ws_server.content_definitions. 
The JSON is made by running a unit test 

python -m wwpdb.apps.tests-contentws.ContentRequestReportIoTests

This outputs a JSON file in the current working directory which can be copied to 
wwpdb.apps.content_ws_server.content_definitions and checked in.

## Registering for access to the API

Access to the API is controlled by a JWT key.
To generate a new key

python -m wwpdb.apps.content_ws_server.register.Register

This will output a key which is needed to access the service

to find more options

python -m wwpdb.apps.content_ws_server.register.Register --help

## Accessing the API

Access to the API is through the onedep-biocuration-api

pip install onedep-biocuration-api