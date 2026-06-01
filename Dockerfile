# Reproducible compute environment for the LLM Jailbreak Taxonomy harness.
#
#   docker build -t jb-tax:4.1.0 .
#   docker run --rm -v "$(pwd)/data/results:/app/data/results" jb-tax:4.1.0
#
# The simulation harness runs offline. For the live API harness, pass:
#   docker run --rm -e ANTHROPIC_API_KEY -e OPENAI_API_KEY ... jb-tax:4.1.0 python evaluate_live.py

FROM python:3.12-slim

LABEL org.opencontainers.image.title="llm-jailbreak-taxonomy"
LABEL org.opencontainers.image.description="Mechanism-grounded taxonomy of 40 LLM jailbreak patterns across 10 categories"
LABEL org.opencontainers.image.source="https://github.com/zakky8/llm-jailbreak-taxonomy"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.version="4.1.0"

WORKDIR /app

# System deps for matplotlib font rendering
RUN apt-get update && apt-get install -y --no-install-recommends \
        fonts-dejavu-core \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first (better build caching)
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy code + data
COPY . .

# Default: run the mock simulation harness with seeded reproducibility
CMD ["python", "evaluate_phase2b.py", "--mock", "--trials", "5", "--seed", "42"]
