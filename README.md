# basic-scraper
## To Use:
First:
```
git clone https://github.com/amosboldor/basic-scraper.git
pip install -e .
```


1. Pass the paramiters you want in the kwargs dictionary in the ```generate_results``` function block
2. Then run and it will print the data and make geojson file called my_map.json

or

1. Put existing html file and name it inspection_page.html
2. Then run with test after "python scraper.py" and it will print the data and make geojson file called my_map.json

Then plug the geojson into http://geojson.io/