import random
from fastapi import FastAPI
from prometheus_client import (
    make_asgi_app,
    disable_created_metrics,
    Summary,
    Histogram,
    Counter,
    Gauge)
import time
from collections import deque

disable_created_metrics()
# Create app
app = FastAPI(debug=False)

# Add prometheus asgi middleware to route /metrics requests
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# some structures for fake activity
de = deque()

# Create a metric to track time spent and requests made.
METHOD_EXECUTION_TIME = Histogram(
    'method_execution_time_seconds',
    'Time spent processing request including overhead',
    buckets=(.01, .025, .05,  .1, .25, .5, 1.0, 2.0, 5.0, 10.0, 15.0, float("inf"))
)
REQUEST_COUNT = Counter('request_count', 'Total requests processed', ['priority', 'category'])
PROCESSING_TIME = Summary('processing_time', 'Time spent on processing only, without overhead', ['priority', 'category'])
QUEUE_SIZE = Gauge('queue_size', 'The number of messages in a queue')
QUEUE_SIZE.set_function(lambda: len(de))

# Decorate function with metric to measure total request processing time
@app.get("/process")
@METHOD_EXECUTION_TIME.time()
def process_request(priority: int = 1, category: str = 'default'):
    # s is a kind of "request"
    s = f"request pri={priority}, category={category}"
    print(s)

    # increase a total request counter
    REQUEST_COUNT.labels(priority, category).inc()
    # put the request into a queue
    de.append(s)
    # simulate a changing length of the queue (with some probability)
    if len(de) > 0 and random.random() > 0.5:
        de.pop()

    # measure actual processing time
    with PROCESSING_TIME.labels(priority, category).time():
        # simulate processing delay
        time.sleep(random.random() * 3)

    # simulate some extra overhead delay (so METHOD_EXECUTION_TIME could differ from PROCESSING_TIME)
    time.sleep(random.random() * 0.3)
