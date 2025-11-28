FROM pandoc/latex

# Install Python3 and pip
RUN apk add --no-cache python3 py3-pip


# Install additional LaTeX packages
RUN tlmgr update --self && \
    tlmgr install preprint titlesec enumitem marvosym

WORKDIR /app

COPY pyproject.toml .

RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"
RUN pip3 install --no-cache-dir pdm-backend
RUN pip3 install --no-cache-dir .

COPY src/ ./src/
COPY templates/ ./templates/

ENTRYPOINT ["python3", "-m", "src.resume_ci_automation"]