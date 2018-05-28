#! /bin/bash

flask initdb

flask run --host=${APP_HOST}
