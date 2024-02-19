#!/bin/bash

# Função recursiva para percorrer os arquivos do diretório
search_keys() {
    local current_dir="$1"
    for file in "$current_dir"/*; do
        if [ -f "$file" ]; then
            if grep -qE "PRIVATE KEY|BEGIN RSA PRIVATE KEY|BEGIN DSA PRIVATE KEY" "$file"; then
                echo "Private key found: $file"
            fi
        elif [ -d "$file" ]; then
            search_keys "$file"
        fi
    done
}

search_keys "$1"
