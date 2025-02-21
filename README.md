# level - Another Multi-Language Version Manager
**Level** is a lightweight and flexible version manager for multiple programming languages. 💯 It allows developers to easily install, switch, and manage different versions of languages using a simple configuration file (`config.yaml`). ⚙


## 🎉 Features 🎉
- **Supports Multiple Languages**: Node.js, Python, PHP, Go, Rust, Ruby, and more via `config.yaml`.
- **Version Management**: Install, uninstall, and switch between different language versions effortlessly.
- **Path Management**: Add and remove external paths for language versions.
- **Simple & Lightweight**: No complex dependencies, just a single executable.
- **Windows Support**: Available for Windows (Win32/Win64).


## 📥 Installation 📥
### Download & Setup
1. Download `level.exe` and `config.yaml` from the [Release Page](https://example.com/releases). 💾
2. Place `level.exe` in a directory included in your system's `PATH`. 🔧
3. Edit `config.yaml` to configure supported languages if needed. 🛠️


## 🚀 Usage 🚀
### Install language at version to bin or specified path.
```sh
level install <language@version>
# Example1: level install nodejs@22.14.0
# Example2: level install nodejs@22.14
# Example3: level install nodejs@22
# Example4: level install nodejs
```

### Uninstall language at version from bin.
```sh
level uninstall <language@version>
# Example: level uninstall nodejs@22.14.0
```

### Use a specific language version or path by creating a symlink.
```sh
level use <target>
# Example1: level use node@22.14.0
# Example2: level use C:\nodejs
```

### List installed language and version from versions.json.
```sh
level list
# Example: level list
```

### Add an external path to versions.json.
```sh
level add <path>
# Example: level add "C:\Go"
```

### Remove an external path from versions.json.
```sh
level remove <path>
# Example: level remove "C:\Go"
```


## 📜 License 📜
**level** © 2025 by MeowSkyKung is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). 🔖


## 💖 Supporting by 💖
- Star Me on GitHub 🌟
- Donate on Ko-Fi ☕
