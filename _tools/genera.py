#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ricostruisce tutto il sito. Uso:  python3 _tools/genera.py"""
import pathlib, subprocess, sys
T = pathlib.Path(__file__).resolve().parent
for passo in ["genera_catalogo.py", "genera_pagine.py", "genera_articoli.py"]:
    r = subprocess.run([sys.executable, str(T / passo)])
    if r.returncode:
        sys.exit(f"ERRORE in {passo}")
print("Sito ricostruito.")
