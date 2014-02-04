import random
import time

from boto import connect_cloudwatch

cloud_watch = connect_cloudwatch()

fake_instance_ids = [1, 2, 3, 4, 5]


def count_failures(count, instance_id):
    cloud_watch.put_metric_data('BLDemo', 'TestFailMetric', value=count, unit='Count')
    print "Logged failure count: " + str(count)


def count_success(count, instance_id):
    cloud_watch.put_metric_data('BLDemo', 'TestSuccessMetric', value=count, unit='Count')
    print "Logged success count: " + str(count)


def log_response_times(statistic_set):
    cloud_watch.put_metric_data('BLDemo', 'TestResponseTimeMetric', statistics=statistic_set, unit='Milliseconds')
    print "Logged the following response data %s" % statistic_set


def simulate_request(failure_chance):
    maybe = random.random()
    wait_time = random.random()
    response_time = int(wait_time * 1000)
    failed = False

    if maybe < failure_chance:
        failed = True

    time.sleep(wait_time)

    return failed, response_time


def main():
    while True:
        fail_count = 0
        success_count = 0

        max_response = None
        min_response = None
        response_count = 0
        response_sum = 0

        start_time = time.time()

        while True:

            if (time.time() - start_time) < 61.0:
                failed, response_time = simulate_request(0.10)
                if failed:
                    fail_count += 1
                else:
                    success_count += 1

                if max_response is None or max_response < response_time:
                    max_response = response_time
                if min_response is None or min_response > response_time:
                    min_response = response_time

                response_count += 1
                response_sum += response_time

            else:
                random_instance = random.choice(fake_instance_ids)
                count_failures(fail_count, random_instance)
                count_success(success_count, random_instance)
                log_response_times({'maximum': max_response, 'minimum': min_response,
                                    'samplecount': response_count, 'sum': response_sum})

                fail_count = 0
                success_count = 0

                max_response = None
                min_response = None
                response_count = 0
                response_sum = 0

                start_time = time.time()

if __name__ == '__main__':
    main()



