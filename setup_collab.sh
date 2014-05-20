#!/bin/bash

git clone https://github.com/excellaco/collab.git -b hackathon
git clone https://github.com/cfpb/collab-staff-directory.git

mv collab/collab/local_settings_template.py collab/collab/local_settings.py

echo "INSTALLED_APPS += ('staff_directory', )" >> collab/collab/local_settings.py
echo "INSTALLED_APPS += ('schedule', )" >> collab/collab/local_settings.py

pip install -r collab/requirements.txt
pip install -r collab/requirements-test.txt

cd collab
ln -s ../collab-staff-directory/staff_directory
ln -s ../schedule
