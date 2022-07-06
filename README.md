# Task

You are supposed to write a python script that will use the Nasdaq RSS news feed and fetch news given a company symbol(For example, to get news for Microsoft, you will enter MSFT, and it goes to Nasdaq(https://www.nasdaq.com/nasdaq-RSS-Feeds) and gets the news as a list of articles as shown on the link: https://www.nasdaq.com/market-activity/stocks/msft/news-headlines.

The option is either to use RSS or web scraping, but the end state is to get news given a ticker input.

The news should be stored in a cache (please use REDIS) running as a docker.

The news is stored as key and value where the key is the company symbol (so MSFT for Microsoft or INTC for intel etc.), and the value is the list of news with timestamps.

The program needs to run via an API, and you must run it as a background process, i.e., a non-blocking API call. Would you please use some queue to put the task on, and then a call back triggered when the job is completed? Please read up: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxii-background-jobs for doing background jobs in flask.

## Documentation
### How does it work?
<p>We are using flask restful and returning json responses, we're using celery for a task queue for async work.

When the task is submitted at /api/news/msft a task id is returned and the task is added to the queue for asynchronous execution, instead of redis having to cache the response it actually just caches the task id, this allows it to just return the same id before the timeout on the cache and the application can just access the same result using the task id from the celery result queue.

The default timeout is set to 180 second, this can be changed in the main file. The application can run both locally and in docker-compose which is the recommended method of deployment, since it's the application in itself stateless running the app to scale could be beneficial,
</p>

<strong>Return Data Structure</strong><br/>
There was a mention of timestamps in the task, hence in the response we're returning two lists nested inside a list, the first one being the news and the second being the timestamp. We could couple the two together and rather complicate the data structure but this seems to be rather simpler. Hence the choice.


### Future Scope

1. Use the docker sdk to make the application self sufficient when running locally. Spinning up the redis and celery queue automatically using multiprocessing or subprocess.
2. Implement logging and discovery operations on which user agents work for the nasdaq website.
3. Design a better data structure in json to return values across endpoints.

### Deployment
1. Docker compose can automate the process if necessary so that a celery worker doesn't have to be started.
```bash
# Docker will build the application and auto-start it running it in -d mode would be more cleaner.
docker-compose up --build
```

2. You can also use the package manually by starting a redis container and a celery worker, necessary commands are listed here
```bash
# Starting docker container for redis -->
docker run -p 6379:6379 -d redis
# Starting celery worker for async
celery -A project.server.tasks.crawler worker --loglevel=info
# This command will install the application dependencies using pip.
pip install -r requirements.txt
# Start flask server
python manage.py run -h 0.0.0.0 # Bind to all interfaces.
```

# Have a question?
Reach out to me "me@mustansirg.in" or drop a message at www.mustansirg.in.
