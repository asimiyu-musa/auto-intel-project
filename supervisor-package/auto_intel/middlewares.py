import random
from scrapy import signals

class RandomUserAgentMiddleware:
    """
    Custom middleware to rotate user-agents for each request from a list
    defined in the project settings.
    """
    def __init__(self, user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        # This classmethod is used by Scrapy to create an instance of the middleware.
        # It correctly loads the USER_AGENTS list from settings.py.
        return cls(user_agents=crawler.settings.get('USER_AGENTS', []))

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader middleware.
        if self.user_agents:
            user_agent = random.choice(self.user_agents)
            request.headers['User-Agent'] = user_agent
            # Uncomment the line below for debugging to see which user-agent is being used
            # spider.logger.debug(f"Using User-Agent: {user_agent}")

# You can keep the other default middleware classes below if you wish,
# but the RandomUserAgentMiddleware is the one that needed fixing.

class AutoIntelDownloaderMiddleware:
    # This is mostly boilerplate and can be left as is.
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)