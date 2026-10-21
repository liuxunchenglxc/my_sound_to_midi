FROM ghcr.io/void-linux/void-glibc-full:20261001r1 AS runner

RUN xbps-install -Suy git bash curl uv ffmpeg6 tree libsndfile-devel fluidsynth base-devel python-devel portaudio-devel && \
    xbps-remove -Oo

# COPY requirements.txt .
RUN uv pip install --system --break-system-packages --no-cache-dir numpy Cython setuptools requests demucs

RUN uv pip install --system --break-system-packages --no-cache-dir --no-build-isolation madmom omnizart
RUN omnizart download-checkpoints

WORKDIR /workspace