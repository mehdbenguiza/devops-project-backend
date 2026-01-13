from flask import Flask, jsonify, request
import logging
from prometheus_flask_exporter import PrometheusMetrics
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource

# Configuration logs structurés
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# Tracing basique (sortie console pour le moment)
resource = Resource(attributes={"service.name": "devops-backend-api"})
trace.set_tracer_provider(TracerProvider(resource=resource))
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
tracer = trace.get_tracer(__name__)

app = Flask(__name__)
metrics = PrometheusMetrics(app)

counter = 0

@app.route('/health', methods=['GET'])
def health():
    with tracer.start_as_current_span("health"):
        logger.info("Requête health reçue")
        return jsonify({"status": "healthy"}), 200

@app.route('/counter', methods=['POST'])
def increment_counter():
    global counter
    with tracer.start_as_current_span("increment_counter"):
        try:
            data = request.get_json() or {}
            increment = data.get('increment', 1)
            counter += increment
            logger.info(f"Compteur incrémenté de {increment}, nouvelle valeur : {counter}")
            return jsonify({"counter": counter}), 200
        except Exception as e:
            logger.error(f"Erreur lors de l'incrément : {str(e)}")
            return jsonify({"error": str(e)}), 400

@app.route('/metrics')
def metrics_endpoint():
    return metrics.export()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
