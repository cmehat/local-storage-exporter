FROM ghcr.io/astral-sh/uv:0.7.19-python3.13-bookworm-slim@sha256:7de393cd47b85a539e91d112f781b573c77ac7aa9fb01d8a76e6c92fef9b7b76 AS builder

COPY . /app
WORKDIR /app

# Install Python in builder stage and copy to final image to maintain consistent Debian base
ENV UV_PYTHON_INSTALL_DIR=/python
RUN uv python install 3.13
RUN uv sync --locked --no-dev # It will create a virtual environment in /app/.venv

FROM debian:bookworm-slim@sha256:6ac2c08566499cc2415926653cf2ed7c3aedac445675a013cc09469c9e118fdd

COPY --from=builder /python /python
COPY --from=builder /app /app
WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "-m", "local_storage_exporter"]