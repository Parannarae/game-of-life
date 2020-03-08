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
ENV USER_NAME "ubuntu"
ENV HOME_DIR /home/${USER_NAME}
USER ${USER_NAME}

WORKDIR ${HOME_DIR}

# setup the game
RUN mkdir src
COPY start_game_of_life.sh .
COPY ./src/* ./src/

CMD ["/bin/bash", "start_game_of_life.sh"]