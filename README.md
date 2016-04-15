# scrapy lianjia
This a project using [scrapy][scrapy_web] to crawl data from [链家网][lianjia_web].

## How to use
1. Change directory to the root directory of this project.
2. Use `scrapy crawl lianjia -o outputs.csv` to save the crawled data into a *.csv*(also support *.json* and *.xml* format) file.

## Some `scrapy` commands for debugging
- `scrapy shell URL` can be used for debugging specific url
- `scrapy crawl lianjia -s LOG_FILE=scrapy.log` will save the logging info into a file

[scrapy_web]: <http://scrapy.org/>
[lianjia_web]: <http://sh.lianjia.com/ershoufang>
