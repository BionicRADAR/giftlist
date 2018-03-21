# giftlist
A gift list tool

A web application for keeping track of gift wishlists for holidays, birthdays,
and the like.

To run locally: heroku local web

To get access to postgresql, make sure /etc/postgresql/9.6/main/pg_hba.conf has the line:
local all postgres  md5

Then run: sudo restart postgres

run postgres with: psql -U postgres

go to /users to see list of users

To migrate database, do: 
python manage.py db migrate
then
python manage.py db upgrade

To push to heroku: git push heroku master
