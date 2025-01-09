# An example of simple python FASTAPI app instrumented with prometheus client
The exposed html page with metrics will be looking like this: [metrics.example](metrics.example)
### List of metrics
- `METHOD_EXECUTION_TIME`: Histogram with custom set buckets. Showing time spent on an execution of a method. _SUM - total amount of seconds, _COUNT - number of samples, the data distributed across buckets respecting each function execution time.
- `REQUEST_COUNT`: Counter. Showing total requests processed, marked with lables `['priority', 'category']`
- `PROCESSING_TIME`: Summary. Showing time spent on request processing only, without overhead, marked with lables `['priority', 'category']`
- `QUEUE_SIZE`: Gauge. Showing current size of a queue.
