#!/bin/bash

# -------------------------------
# 1️⃣ Create and activate venv
# -------------------------------
python3 -m venv venv
source venv/bin/activate

# -------------------------------
# 2️⃣ Upgrade pip, setuptools, wheel
# -------------------------------
python -m pip install --upgrade pip setuptools wheel

# -------------------------------
# 3️⃣ Install Rust (needed for pydantic-core)
# -------------------------------
if ! command -v cargo &> /dev/null
then
    echo "Installing Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source $HOME/.cargo/env
else
    echo "Rust already installed"
fi
rustup update

# -------------------------------
# 4️⃣ Install PostgreSQL dev libs
# -------------------------------
brew install postgresql openssl || echo "Postgres/OpenSSL may already be installed"

# Set OpenSSL env vars for psycopg2 compilation
export LDFLAGS="-L/opt/homebrew/opt/openssl/lib"
export CPPFLAGS="-I/opt/homebrew/opt/openssl/include"
export PKG_CONFIG_PATH="/opt/homebrew/opt/openssl/lib/pkgconfig"

# -------------------------------
# 5️⃣ Set PYO3 workaround for pydantic-core
# -------------------------------
export PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1

# -------------------------------
# 6️⃣ Install requirements
# -------------------------------
python -m pip install --upgrade pip
python -m pip install -r requirements.txt --no-cache-dir

echo "✅ Setup complete! Activate venv with: source venv/bin/activate"
