# hash:sha256:c84acf04530416d6ee33406bfe6ae3480b9e4037e6bd65a3716934164d6b98ca
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

RUN pip install -U --no-cache-dir \
    pydantic-settings==2.9.1 \
    -e git+https://github.com/AllenNeuralDynamics/aind-analysis-results.git@14df02b6909085f00cbb58d01a66a2c85e5cef6e#egg=aind-analysis-results

COPY postInstall /
RUN /postInstall
