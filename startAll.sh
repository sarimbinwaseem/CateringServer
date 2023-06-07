#!/bin/bash

sudo supervisorctl reload
sudo systemctl start nginx.service
