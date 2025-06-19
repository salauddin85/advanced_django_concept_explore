from memory_profiler import memory_usage

class MemoryLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        mem_before = memory_usage()[0]
        response = self.get_response(request)
        mem_after = memory_usage()[0]
        print(f"🔍 Memory Used: {mem_after - mem_before:.2f} MB")
        return response
