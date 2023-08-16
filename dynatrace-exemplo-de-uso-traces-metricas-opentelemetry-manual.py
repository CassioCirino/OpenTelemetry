import time
import random

from opentelemetry import trace

from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

from opentelemetry.sdk.metrics.export import AggregationTemporality, PeriodicExportingMetricReader
from opentelemetry.sdk.metrics import MeterProvider, Counter

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

from opentelemetry.metrics import set_meter_provider, get_meter_provider


# Substitua pelas informações do Dynatrace
DT_API_URL = 'sua url de ambiente aqui'
DT_API_TOKEN = 'seu api token aqui' # O escopo do token deve conter metrics.ingest openTelemetryTrace.ingest, caso a solucao pretendida envolva log o escopo logs.ingest deve ser acrescentado.

# Criação do provedor de traces
tracer_provider = TracerProvider()

# Configuração do provedor global de traces
trace.set_tracer_provider(tracer_provider)

# Criação de um exportador de traces OTLP para o Dynatrace
trace_exporter = OTLPSpanExporter(
    endpoint=DT_API_URL + "/v1/traces",
    headers={"Authorization": "Api-Token " + DT_API_TOKEN},
)

# Configuração do processador de spans e exportador de traces
tracer_provider.add_span_processor(
    SimpleSpanProcessor(trace_exporter)
)

# Criação de um exportador de métricas do Dynatrace
exporter = OTLPMetricExporter(
    endpoint=DT_API_URL + "/v1/metrics",
    headers={"Authorization": "Api-Token " + DT_API_TOKEN},
    preferred_temporality={Counter: AggregationTemporality.DELTA}
)

# Criação de um leitor de métricas para exportação periódica
reader = PeriodicExportingMetricReader(exporter)

# Criação de um provedor de métricas
metrics_provider = MeterProvider(metric_readers=[reader])

# Configuração do provedor global de métricas
set_meter_provider(metrics_provider)

# Obtém o medidor
meter = get_meter_provider().get_meter(__name__)

# Nomes fictícios do mundo real para especialidades, exames, diagnósticos e medicamentos
especialidades = [
    "Cardiologia", "Dermatologia", "Ortopedia", "Oftalmologia", "Pediatria",
    "Ginecologia", "Oncologia", "Neurologia", "Endocrinologia", "Urologia"
]

exames = [
    "Ressonancia Magnetica", "Tomografia Computadorizada", "Eletrocardiograma",
    "Ultrassom", "Colonoscopia", "Hemograma", "Radiografia", "Mamografia", "Endoscopia",
    "Holter"
]

diagnosticos = [
    "Hipertensao", "Diabetes Tipo 2", "Fratura de Tornozelo", "Alergia a Amendoim",
    "Conjuntivite", "Gripe", "Cancer de Mama", "Enxaqueca", "Hipotireoidismo",
    "Infeccao do Trato Urinario"
]

medicamentos = [
    "Aspirina", "Metformina", "Paracetamol", "Ibuprofeno", "Antialergico",
    "Antibiotico", "Analgesico", "Insulina", "Levotiroxina", "Anti-inflamatorio"
]

# Dicionário para armazenar métricas
metrics_dict = {}

# Loop infinito para simular atendimentos
while True:
    # Geração de dados aleatórios
    paciente_nome = f'Paciente {random.randint(1, 100)}'
    especialidade_medica = random.choice(especialidades)
    exames_realizados = random.choice(exames)
    diagnostico = random.choice(diagnosticos)
    medicamento = random.choice(medicamentos)

    # Criação de spans para cada etapa do atendimento
    with trace.get_tracer(__name__).start_as_current_span("Especialidade"):
        print(f"Atendimento: {paciente_nome}, Etapa: {especialidade_medica}")
        metric = metrics_dict.get(especialidade_medica)
        if metric:
            metric.add(1)
        with trace.get_tracer(__name__).start_as_current_span("Exames"):
            print(f"Atendimento: {paciente_nome}, Etapa: {exames_realizados}")
            metric = metrics_dict.get(exames_realizados)
            if metric:
                metric.add(1)
            with trace.get_tracer(__name__).start_as_current_span("Diagnostico"):
                print(f"Atendimento: {paciente_nome}, Etapa: {diagnostico}")
                metric = metrics_dict.get(diagnostico)
                if metric:
                    metric.add(1)
                with trace.get_tracer(__name__).start_as_current_span("Medicamento"):
                    print(f"Atendimento: {paciente_nome}, Etapa: {medicamento}")
                    metric = metrics_dict.get(medicamento)
                    if metric:
                        metric.add(1)

    # Aguarda um tempo para simular o próximo atendimento
    time.sleep(random.randint(3, 10))