#!/bin/bash
set -euo pipefail
datasette --reload --plugins-dir plugins/
