#!/bin/bash

# set up local stack of supabase
# TODO: is there a way to only link to remote without setting up all the containers
supabase init
supabase start

supabase link

# 