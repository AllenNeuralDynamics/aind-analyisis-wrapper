# hash:sha256:5a23caf176de7a025e1e25dc2f1af71ea6b6362dc232312b436d258d8f8a3a45
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/mambaforge3:24.5.0-0-python3.12.4-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN pip install -U --no-cache-dir \
    pydantic-settings==2.9.1 \
    -e git+https://github.com/AllenNeuralDynamics/aind-analysis-results.git@adce05f3b7b1320b83c6d93937fbc2c9100ca6d0#egg=aind-analysis-results

COPY postInstall /
RUN /postInstall
