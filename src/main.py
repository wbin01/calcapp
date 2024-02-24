#!/usr/bin/env python3
import pathlib
import sys

import streamlit as st

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR.as_posix())

if __name__ == '__main__':
	st.switch_page('pages/home.py')
