from db.create_database import Db
from crawler.spider import Spider

if __name__ == "__main__":
    db = Db()
    # 开始第一次爬取时的初始化
    db.insert_first()
    spider = Spider(db)
    spider.start()
