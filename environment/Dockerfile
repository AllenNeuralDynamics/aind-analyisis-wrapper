# hash:sha256:6071b56302fadc172543aca8ea0379068b163091f40d5dc25ebdcc0fb9abecd0
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/mambaforge3:24.5.0-0-python3.12.4-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG AWS_ACCESS_KEY_ID
ARG AWS_DEFAULT_REGION
ARG AWS_SECRET_ACCESS_KEY
ARG CODEOCEAN_API_TOKEN
ARG CODEOCEAN_DOMAIN

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

ENV DOCDB_HOST=api.allenneuraldynamics-test.org
ENV DOCDB_DATABASE=analysis
ENV DOCDB_COLLECTION=processing_v2

RUN pip install -U --no-cache-dir \
    pydantic-settings==2.9.1 \
    -e git+https://github.com/AllenNeuralDynamics/aind-analysis-results.git#egg=aind-analysis-results

COPY postInstall /
RUN /postInstall
