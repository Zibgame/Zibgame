#!/bin/bash

set -e

echo "Mise à jour des paquets et installation des dépendances..."
sudo apt update
sudo apt install -y ninja-build gettext libtool libtool-bin autoconf automake cmake g++ pkg-config unzip curl doxygen git

echo "Suppression d’une éventuelle ancienne version source de Neovim..."
rm -rf ~/neovim

echo "Clonage du dépôt Neovim..."
git clone https://github.com/neovim/neovim.git ~/neovim

cd ~/neovim

echo "Passage sur la branche nightly..."
git checkout nightly

echo "Compilation de Neovim (cela peut prendre plusieurs minutes)..."
make CMAKE_BUILD_TYPE=RelWithDebInfo

echo "Installation de Neovim (sudo requis)..."
sudo make install

echo "Neovim installé !"

echo "Installation de LazyVim..."
# Suppression d'une ancienne config LazyVim si existante
rm -rf ~/.config/nvim

# Cloner LazyVim (version officielle)
git clone https://github.com/LazyVim/starter ~/.config/nvim

echo "Installation de ta config custom depuis Vim-Config..."

# Cloner ton repo de config
git clone https://github.com/Zibgame/Vim-Config.git ~/Vim-Config

# Copier la config custom par-dessus
cp -r ~/Vim-Config/Vim-Config/* ~/.config/nvim/

# Supprimer les métadonnées git
rm -rf ~/.config/nvim/.git

# Supprimer le dossier cloné
rm -rf ~/Vim-Config

echo "Installation terminée ! Lance Neovim avec la commande : nvim"

