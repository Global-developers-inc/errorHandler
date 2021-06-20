#!/bin/bash

journalctl -o json-pretty -n 50 > out.json
curl -d @out.json -X POST http://localhost:5000/