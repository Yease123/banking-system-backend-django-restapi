from rest_framework.throttling import UserRateThrottle
from rest_framework.exceptions import Throttled

class changeBankthrottle(UserRateThrottle):
    scope='changeBank'
    def throttle_failure(self):
        # Custom error message when rate limit is exceeded
        raise Throttled(detail="You have exceeded the allowed number of request Try tommrrow")