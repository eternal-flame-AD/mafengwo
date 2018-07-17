# mafengwo

一个基于scrapy框架编写的[马蜂窝](http://www.magengwo.cn/)用户旅游路线爬虫，核心代码不到50行！

一天成功爬取25万用户足迹~

使用方法:

```sh
$pip install -r requirements.txt
$scrapy crawl path -o dests.json
```

PS: 虽然马蜂窝还在很辣鸡地使用http，还是不要过于密集地爬取，<s>象征性地</s>给服务器0.1s的休息时间
