# Kali Mirror Manager

Kali Mirror Manager is a Python command-line tool designed to manage mirrors for the Kali Linux distribution. It allows users to ping mirrors to measure latency, and set a new mirror for package updates.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/0xtamsee1/kali-mirror-manager.git
   ```
2. Navigate to the project directory:
   ```bash
   cd kali-mirror-manager
   ```
3. Run the script:
   ```bash
   python3 mirror_manager.py
   ```
## Usage

Once you run the script, you'll be presented with a command-line menu with options:

- **menu**: Display commands and usage
- **show**: Display the list of available mirrors
- **ping**: Ping all mirrors to measure latency
- **set**: Set a new mirror for package updates
- **exit**: Terminate the session

### Setting a New Mirror

To set a new mirror, use the `set` command followed by the mirror URL. For example:

```bash
cmd> set http://http.kali.org/kali
```
