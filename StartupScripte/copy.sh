#!/bin/bash

#Script 06/2024 Tatjana Baier

scp -i .ssh/id_dsa -r data/*  ubuntu@ec2-54-147-146-174.compute-1.amazonaws.com:/home/ubuntu/data/
