# Game of Life
A python program to play the game of life. Description of the game can be found in the [wiki](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) page.

## Prerequisite
- [docker](https://www.docker.com/)

# Quick Guide
## Interactive mode
1. install the game

```bash
docker-compose build
```

2. run the game and play

```bash
docker-composer run main
```

## None-interactive mode
1. install the game

```bash
docker-compose build
```

2. place the initial file under the directory `shared_folder`

3. run the game (assuming the initial file name `initial_file.txt`)

```bash
docker-compose run main initial_file.txt 5
```

# Installation
Install can be done using `docker-compose` command:

```bash
docker-compose build
```

# Instruction to Play
Program can be started using `docker-compose`:

```bash
# {arguments} part is used to determine the play mode
docker-compose run main {arguments}
```
## Play mode
There are three ways to start up this program

1. Interactive mode with random initial setting
2. Interactive mode with given initial setting (using a text file)
3. Non-interactive mode with given initial setting (using a text file)

### Mode 1 (Interactive Mode with Random)
If no `arguments` is given, the program is running in the interactive mode with random initial setting:

```bash
docker-compose run main
```

In this mode, the size of the board and initial live cells are randomly assigned.

### Mode 2 (Interactive Mode with Initial setting)
If one `arguments` is given, the program is running in the interactive mode with given initial setting:

```bash
# {file_name} is the name of the file to load the file should be under `./shared_folder`
docker-compose run main {file_name}
```

In this mode, the size of the board and initial live cells are assigned according to the file `{file_name}`. This file should be placed under `shared_folder`, and refer to `File Format` session for the detailed description of the file.

### Mode 3 (Non-interactive Mode with Initial setting)
If two `arguments` is given, the program is running in non-interactive mode with given initial setting:

```bash
# {file_name} is the name of the file to load and the file should be under .`/shared_folder`
# {number_of_generations} is the number of the generation to progress before creating file output
docker-compose run main {file_name} {number_of_generations}
```

In this mode, the program creates `result_dump.txt` file under `shared_folder` directory, which contains the information of the board after `{number_of_generations}` steps.

Like mode 2, `{file_name}` file defines the initial status of the board, and this file should be placed under `shared_folder`. Refer to `File Format` session for the detailed description of the file.

# File Format
**NOTE: all files should be placed under the directory `shared_folder`** 

The input file, containing the initial board status, and the output file, containing the result of the board, is formatted as follows:

```
board_height board_width
total_number_of_alive_cells
row_index_of_first_alive_cell column_index_of_first_alive_cell
row_index_of_second_alive_cell column_index_of_second_alive_cell
...
```

Note that the number of lines from line 3 to end of the line should be same as `total_number_of_alive_cells`.