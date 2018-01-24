# giftlist
A gift list tool

To run locally: heroku local web

To get access to postgresql, make sure /etc/postgresql/9.6/main/pg_hba.conf has the line:
local all postgres  md5

Then run: sudo restart postgres

run postgres with: psql -U postgres

go to /userlist to see list of users

To migrate database, run flask db upgrade

To push to heroku: git push heroku master
