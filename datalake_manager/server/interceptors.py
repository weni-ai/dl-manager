import grpc
from limits import RateLimitItem, parse
from limits.storage import MemoryStorage
from limits.strategies import MovingWindowRateLimiter


class RateLimiterInterceptor(grpc.ServerInterceptor):
    """
    A gRPC interceptor that provides granular rate limiting for incoming requests
    based on the gRPC service being called.
    """

    def __init__(
        self,
        default_rate_limit: str,
        service_rate_limits: dict[str, str] | None = None,
    ):
        """
        Initializes the interceptor with specific limits for each service.
        Args:
            default_rate_limit: The fallback rate limit for services that
                                do not have a specific limit defined.
            service_rate_limits: A dictionary mapping full service names to
                                 rate limit strings (e.g., "100/minute").
        """
        self.default_rate_limit_item = parse(default_rate_limit)
        self.service_rate_limit_items = {
            service: parse(limit_str)
            for service, limit_str in (service_rate_limits or {}).items()
        }
        self.storage = MemoryStorage()
        self.limiter = MovingWindowRateLimiter(self.storage)

    def intercept_service(self, continuation, handler_call_details):
        """
        Intercepts an incoming RPC to apply service-specific rate limiting.
        """
        # e.g., /package.Service/Method
        method_name = handler_call_details.method
        try:
            # ['', 'package.Service', 'Method'] -> 'package.Service'
            service_name = method_name.split("/")[1]
        except IndexError:
            # Should not happen on valid RPCs. Fallback to default limit
            # using the full method name as a key.
            rate_limit_item = self.default_rate_limit_item
            key = method_name
        else:
            # Use the specific service rate limit if it exists, otherwise, the default.
            # The key for the limiter is the service name, so all methods within
            # that service share the same rate limit bucket.
            rate_limit_item = self.service_rate_limit_items.get(
                service_name, self.default_rate_limit_item
            )
            key = service_name

        if not self.limiter.hit(rate_limit_item, key):

            def abort_handler(_request, context):
                context.abort(
                    grpc.StatusCode.RESOURCE_EXHAUSTED,
                    f"Rate limit for service {key} exceeded. "
                    f"The limit is {str(rate_limit_item).replace('/', ' per ')}.",
                )

            return grpc.unary_unary_rpc_method_handler(abort_handler)

        return continuation(handler_call_details)
