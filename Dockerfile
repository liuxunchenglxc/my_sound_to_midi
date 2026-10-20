FROM ghcr.io/void-linux/void-glibc-full:20261001r1 AS runner

RUN xbps-install -Suy git bash curl uv ffmpeg6 tree && \
    xbps-remove -Oo

COPY requirements.txt .
RUN uv pip install --system --break-system-packages --no-cache-dir -r requirements.txt && omnizart download-checkpoints

WORKDIR /workspace