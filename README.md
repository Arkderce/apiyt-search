
### Description
Code is designed to look for new videos in youtube and notify user about found ones.
 
Used libs:                                                                        
 PYWIN32                                                                           
   For notification popup    !!!WORKS ONLY FOR WINDOWS!!!                                                                                                                                     
 YOUTUBE API v3                                                                    
   To search new videos on youtube.com  

### Usage 
Install pywin32 from link:
https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/                                            
                                   
Install youtube api v3:
```sh
$ pip install --upgrade google-api-python-client
```

Requires DEVELOPER KEY from google
get it from code.google.com/apis/console
paste it into main.py
                                                                                                                                                                     
To write keyword put in console 
```sh
$ python main.py --q YOURKEYWORD
```

To open browser after notification put in console
```sh
$ python main.py --open-browser 1
```

### Tips
If you need titles from youtube its good to encode them with:
`value.encode('utf-8')`