# Start from Ubuntu 16.04
FROM ubuntu:16.04

# Install required packages and clean up the apt cache
RUN apt-get update && apt-get install --no-install-suggests -y \
    python3 \
    vim

# Clean up the apt cache and temporary files
RUN rm -rf /temp \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Add non root user
RUN adduser --disabled-password --gecos '' ubuntu

# Work with a non-root user for security
ARG USER_NAME="ubuntu"
USER ${USER_NAME}

WORKDIR /home/${USER_NAME}

# setup the game
RUN mkdir src tests shared_folder
COPY ./src/* ./src/
COPY ./tests/* ./tests/

ENTRYPOINT [ "python3", "src/game_of_life.py" ]