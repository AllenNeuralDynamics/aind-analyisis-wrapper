# hash:sha256:3748bea15e25eab75bd642644d5f97b454bde50acddd578eb3e448e556df9001
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/mambaforge3:24.5.0-0-python3.12.4-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG CUSTOM_KEY
ARG CUSTOM_KEY_2

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN pip install -U --no-cache-dir \
    pydantic-settings==2.9.1 \
    -e git+https://github.com/AllenNeuralDynamics/aind-analysis-results.git@adce05f3b7b1320b83c6d93937fbc2c9100ca6d0#egg=aind-analysis-results

COPY postInstall /
RUN /postInstall
