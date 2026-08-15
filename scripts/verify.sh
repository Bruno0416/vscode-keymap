#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python3 scripts/generate_keymaps.py
python3 scripts/validate_keymaps.py
python3 scripts/report_coverage.py
./gradlew --no-configuration-cache test verifyPluginProjectConfiguration verifyPluginStructure
