#!/bin/bash

act -W .github/workflows/ci.yml -j checks --matrix python-version:3.11
