# hash:sha256:11ac7780f6a3afae77b8bafc8a779386f26ef25d0cdc43b49a28c6b48c8be474
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/mambaforge3:24.5.0-0-python3.12.4-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG AWS_ACCESS_KEY_ID
ARG AWS_DEFAULT_REGION
ARG AWS_SECRET_ACCESS_KEY
ARG CODEOCEAN_API_TOKEN

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

ENV DOCDB_HOST=api.allenneuraldynamics-test.org
ENV DOCDB_DATABASE=analysis
ENV DOCDB_COLLECTION=processing_v2
ENV CODEOCEAN_DOMAIN=https://codeocean.allenneuraldynamics.org/
ENV CODEOCEAN_EMAIL=tom.chartrand@alleninstitute.org

RUN pip install -U --no-cache-dir \
    pydantic-settings==2.9.1 \
    s3fs==0.4.2 \
    -e git+https://github.com/AllenNeuralDynamics/aind-analysis-results.git@c64c0526d3b6ed4b8a1aa9334698a810b560607d#egg=aind-analysis-results

COPY postInstall /
RUN /postInstall
