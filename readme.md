Foo bar
==============









## Running on Nginx

### CGI
Here's an Nginx FastCGI configuration for Ubuntu based on the
[Arch Linux Wiki](https://wiki.archlinux.org/index.php/Nginx#FastCGI).

Install.

    apt-get install fcgiwrap nginx

Configure the nginx site.
                                                  
    location / {                                               
        fastcgi_param DOCUMENT_ROOT /var/www/;
        fastcgi_param SCRIPT_NAME sqlite_api.py;
        fastcgi_pass unix:/var/run/fcgiwrap.socket;
    }

This depends on `/var/www/sqlite_api.py` being a cgi script file that www-data
can execute.

Then (re)start the daemons.

    service fcgiwrap restart
    service nginx restart

### uWSGI
Here's a configuration based on the
[uWSGI quickstart]h(ttp://projects.unbit.it/uwsgi/wiki/Quickstart)

Install these.

    apt-get install uwsgi nginx uwsgi-plugin-{http,python}  

Run this (preferably as a daemon).

    uwsgi \
      --plugins http,python \
      --wsgi-file sqlite_api.py \
      --socket 127.0.0.1:3031 \
      --callable application \
      --processes 20

We'll have to adjust the api script so that it works with uWSGI;
`sqlite_api.py` is that.

Add this to the nginx site. (Try /etc/nginx/sites-enabled/default)

    location /path/to/sqlite {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:3031;
    }

Restart nginx.

    service nginx restart

Test

    curl localhost/path/to/sqlite?q=SELECT+42+FROM+sqlite_master

## Add later
Gzip responses.
