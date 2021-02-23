# jpbeetles-crawler
[日本産甲虫全種目録2020年版](https://japanesebeetles.jimdofree.com/目録/)から自動で甲虫の分類情報を取得するスクリプトです

## 使い方
pipenv環境は構築済みとします

```
pipenv install
```

```cd jpbeetles/jpbeetles/spiders
```

scrapy crawl taxa -o .csv(または.json)
```
