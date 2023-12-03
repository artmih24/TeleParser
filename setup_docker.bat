call docker build -t teleparser .
call docker container create teleparser
call docker container run teleparser