#!/bin/bash
# Pide setup script - Auto-install dependencies based on system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

echo_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

echo_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    else
        OS="unknown"
    fi
    echo_info "Detected OS: $OS"
}

# Detect Linux distribution
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO=$ID
    elif [ -f /etc/debian_version ]; then
        DISTRO="debian"
    elif [ -f /etc/fedora-release ]; then
        DISTRO="fedora"
    elif [ -f /etc/arch-release ]; then
        DISTRO="arch"
    else
        DISTRO="unknown"
    fi
    echo_info "Detected distribution: $DISTRO"
}

# Install system dependencies for Linux
install_system_deps() {
    if [ "$OS" != "linux" ]; then
        echo_info "macOS detected - system dependencies should be handled by Homebrew if needed"
        return 0
    fi

    echo_info "Installing system dependencies for PySide6..."
    echo_warn "This may require sudo privileges"

    case $DISTRO in
        ubuntu|debian)
            echo_info "Using apt-get (Ubuntu/Debian)"
            if ! sudo apt-get update -qq; then
                echo_warn "apt-get update failed, continuing anyway..."
            fi
            sudo apt-get install -y \
                python3-pip \
                python3-venv \
                libxcb1 \
                libxcb-xinerama0 \
                libxcb-cursor0 \
                libxcb-xfixes0 \
                libxcb-xkb1 \
                libxkbcommon-x11-0 \
                libxkbcommon0 \
                libxcb-render0 \
                libxcb-shm0 \
                libxcb-icccm4 \
                libxcb-image0 \
                libxcb-keysyms1 \
                libxcb-randr0 \
                libxcb-render-util0 \
                libxcb-shape0 \
                libxcb-sync1 \
                libxcb-xinput0 \
                libxrender1 \
                libfontconfig1 \
                libx11-6 \
                libx11-xcb1 \
                libxext6 \
                libxfixes3 \
                libxi6 2>/dev/null || {
                    echo_warn "Some packages may have failed to install, but continuing..."
                }
            ;;
        fedora|rhel|centos)
            echo_info "Using dnf (Fedora/RHEL/CentOS)"
            sudo dnf install -y \
                python3-pip \
                python3-devel \
                libxcb \
                xcb-util \
                xcb-util-image \
                xcb-util-keysyms \
                xcb-util-renderutil \
                xcb-util-wm \
                libxkbcommon \
                libxkbcommon-x11 2>/dev/null || {
                    echo_warn "Some packages may have failed to install, but continuing..."
                }
            ;;
        arch|manjaro)
            echo_info "Using pacman (Arch/Manjaro)"
            sudo pacman -S --noconfirm \
                python \
                python-pip \
                libxcb \
                xcb-util \
                xcb-util-image \
                xcb-util-keysyms \
                xcb-util-renderutil \
                xcb-util-wm \
                libxkbcommon \
                libxkbcommon-x11 2>/dev/null || {
                    echo_warn "Some packages may have failed to install, but continuing..."
                }
            ;;
        *)
            echo_warn "Unknown distribution: $DISTRO"
            echo_warn "Please install PySide6 system dependencies manually if needed."
            echo_warn "See README.md for instructions."
            ;;
    esac
    
    echo_info "System dependencies installation completed"
}

# Install Python dependencies
install_python_deps() {
    echo_info "Installing Python dependencies using $PYTHON_CMD..."

    # Check if uv is available
    if command -v uv > /dev/null 2>&1; then
        echo_info "Using uv for faster dependency installation"
        if ! uv pip install -r requirements.txt; then
            echo_error "Failed to install dependencies with uv"
            exit 1
        fi
    elif $PYTHON_CMD -m pip --version > /dev/null 2>&1; then
        echo_info "Using $PYTHON_CMD -m pip"
        if ! $PYTHON_CMD -m pip install --user -r requirements.txt; then
            echo_error "Failed to install dependencies with $PYTHON_CMD -m pip"
            exit 1
        fi
    elif command -v pip3 > /dev/null 2>&1; then
        echo_info "Using pip3"
        if ! pip3 install --user -r requirements.txt; then
            echo_error "Failed to install dependencies with pip3"
            exit 1
        fi
    elif command -v pip > /dev/null 2>&1; then
        echo_info "Using pip"
        if ! pip install --user -r requirements.txt; then
            echo_error "Failed to install dependencies with pip"
            exit 1
        fi
    else
        echo_error "No Python package manager found (pip/pip3/uv)"
        echo_info "Trying to install pip: $PYTHON_CMD -m ensurepip --upgrade"
        if ! $PYTHON_CMD -m ensurepip --upgrade; then
            echo_error "Failed to install pip. Please install pip manually."
            exit 1
        fi
        $PYTHON_CMD -m pip install --user -r requirements.txt
    fi
    
    echo_info "Python dependencies installed successfully"
}

# Check Python version
check_python() {
    # Try to find Python 3.10+ in order of preference
    PYTHON_CMD=""
    
    # Check for specific versions first (python3.12, python3.11, python3.10)
    for version in 12 11 10; do
        if command -v python3.$version > /dev/null 2>&1; then
            PYTHON_VERSION=$(python3.$version --version 2>&1 | awk '{print $2}')
            MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
            MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
            if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 10 ]; then
                PYTHON_CMD="python3.$version"
                echo_info "Found Python: $PYTHON_VERSION (python3.$version)"
                export PYTHON_CMD
                return 0
            fi
        fi
    done
    
    # Fallback to python3 or python
    if command -v python3 > /dev/null 2>&1; then
        PYTHON_CMD="python3"
    elif command -v python > /dev/null 2>&1; then
        PYTHON_CMD="python"
    else
        echo_error "Python not found. Please install Python 3.10+"
        echo_info "Installation instructions:"
        echo_info "  macOS: brew install python@3.11"
        echo_info "  Ubuntu/Debian: sudo apt-get install python3.10 python3.10-venv python3.10-pip"
        echo_info "  Fedora: sudo dnf install python3.11"
        exit 1
    fi

    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    echo_info "Found Python: $PYTHON_VERSION"

    # Check if version is 3.10+
    MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 10 ]); then
        echo_error "Python 3.10+ required, but found $PYTHON_VERSION"
        echo_info ""
        echo_info "Please install Python 3.10 or higher:"
        echo_info "  macOS:"
        echo_info "    brew install python@3.11"
        echo_info "    # Then use: python3.11 -m pide"
        echo_info ""
        echo_info "  Ubuntu/Debian:"
        echo_info "    sudo apt-get update"
        echo_info "    sudo apt-get install python3.10 python3.10-venv python3.10-pip"
        echo_info ""
        echo_info "  Fedora/RHEL:"
        echo_info "    sudo dnf install python3.11"
        echo_info ""
        echo_info "  Or check if python3.10/python3.11/python3.12 is already installed:"
        echo_info "    which python3.10 python3.11 python3.12"
        exit 1
    fi
    
    export PYTHON_CMD
}

# Main setup
main() {
    echo_info "Setting up Pide..."
    
    check_python
    detect_os
    if [ "$OS" == "linux" ]; then
        detect_distro
        install_system_deps
    fi
    install_python_deps
    
    echo_info "Setup complete!"
    echo_info "Run 'make run' or './run-pide' to start."
    echo_info "Or use: $PYTHON_CMD -m pide"
}

main "$@"
