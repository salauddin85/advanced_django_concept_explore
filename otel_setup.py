from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.django import DjangoInstrumentor

# Set provider
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Exporter to Jaeger
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",  # Jaeger running locally
    agent_port=6831,
)

# Add processor
span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrument Django
DjangoInstrumentor().instrument()
