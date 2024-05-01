#!/bin/bash

echo "Deploy FavLinks to AppEngine"
cd favlinks/
gcloud config set project favlinks
gcloud app deploy
gcloud app describe


echo "  gcloud app open-console\
  gcloud app update\
  gcloud app logs tail\
  gcloud access-approval requests approve"
