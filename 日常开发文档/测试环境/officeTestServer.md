1. ip 
    initial : 192.168.1.243
        ## to be changed 
    
2. user / pass
    root / guoku!@#
    Jiaxiaoke / 1
    
    

3. mysql (install mysql )
    user / pass
    root / mypass
    
4. copy requirements to /opt/script/requirements

    brew install pip 
    brew install freetype imagemagick
    pip install -r requirements
    pip install qrcode 
    
 
5. brew install redis
    bash > redis-server &
    
6. start redis 
    redis-server 
   
### can use file cache instead of redis cache 
 
   
7. start mysql  , 
  su first or ...
  sudo /usr/local/mysql/support-files/mysql.server start
  
  make sure your mysql server has user/pass same as the office.py settings file 
  
  
8. code in /data/www/nut 
   
9. deploy 
  
   in deploy folder, run : 

   fab -f upload_local_test.py upload 
   
   ### ip address and folder setup see local_test_config.ini

10. start server 

    in /data/www/nut 
    run: 
    sudo , or su 
    
    gunicorn -b 0.0.0.0:80 office -w 3 &

    
    stop server 
    need dig out ..... 
    
    current just
     a. ps aux | grep gunicorn 
     b. kill -9 pid of the process last command showed 
     
     
    
11, 办公室果库＋ for TEST SERVER 
    a. in chrome add a bookmark 
    b. edit the bookmark's address to :

    
    c. goto a taobao entity page 
    d. press  办公室果库＋  
    F. you should able to add entity now 
    
    
    
reference : 

https://www.digitalocean.com/community/tutorials/how-to-deploy-python-wsgi-apps-using-gunicorn-http-server-behind-nginx
    
    
    
    
   
 
 