# Snake Game

This is a simple terminal-based Snake game implemented in Python using the `curses` library.

## Features:
- Terminal-based snake game.
- Randomly generated apples for the snake to eat.
- Snake grows longer as it eats apples.
- Use W, A, S, D keys to control the snake.
- Press `q` to quit the game.

## Requirements:
- Python 3.x
- Libraries:
  - `curses`: For handling terminal input and output.
  - `random`: For generating random positions for food (comes pre-installed with Python).
  - `time`: For managing delays (comes pre-installed with Python).

### Installing Dependencies

#### **1. For Linux:**
On most Linux distributions, the `curses` library is included by default with Python. If it’s missing or you encounter any issues, you can install it manually.
```bash
sudo apt install python3-curses
  ```


#### **2. For macOS:**
On macOS, `curses` is usually included with Python. If you are using `Homebrew` to manage packages, you can ensure it's installed as follows:
```bash
brew install ncurses
  ```


#### **3. For Windows:**
The `curses` library is not available natively on Windows. You need to install the `windows-curses` package to make it work.
```bash
pip install windows-curses
  ```


### How to run:
```bash
git clone https://github.com/mahdinetk/snake-game.git
cd snake-game
python3 game.py
  ```

## Controls:
- **W**: Move up
- **A**: Move left
- **S**: Move down
- **D**: Move right
- **Q**: Quit the game
