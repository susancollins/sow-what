FROM ghcr.io/prefix-dev/pixi:0.45.0

RUN apt-get update \
    && apt-get install -y build-essential git make miller \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists* /tmp/* /var/tmp/*

RUN git config --global --add safe.directory '*'

# Pixi does not seem to like being run from root
WORKDIR /app

# Simulate "pixi shell" without using CMD or ENTRYPOINT
ENV PATH="/app/.pixi/envs/dev/bin:$PATH"
ENV PYTHONPATH="/app/.pixi/envs/dev/lib/python3.12/site-packages:/app"

# Install dependencies, sow-what installed as editable
COPY pyproject.toml pixi.lock ./
RUN pixi install -e dev --locked && rm -rf ~/.cache/rattler
COPY . .