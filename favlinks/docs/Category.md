# Category

You can manage system categories using Django Admin command. 

This lising shows how to list categories and add some new ones:
```
python manage.py category list
python manage.py category add --name travel
python manage.py category add --name food
python manage.py category add --name news
python manage.py category add --name technology  
```

To delete 'travel'
```
python manage.py category delete --name travel
```