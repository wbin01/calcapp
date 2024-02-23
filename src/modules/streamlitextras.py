#!/usr/bin/env python3
import os
import pathlib

import streamlit as st

BASE_DIR = pathlib.Path(__file__).resolve().parent


class StreamlitExtras(object):
	def __init__(self) -> None:
		"""..."""
		self.set_local_css()
		self.set_remote_css()

	@staticmethod
	def disable_sidebar() -> None:
		"""
		Only works if 'initial_sidebar_state' param of set_page_config is
		setting as "collapsed"
		"""
		st.markdown("""
			<style>[data-testid="collapsedControl"] {display: none}</style>""",
			unsafe_allow_html=True)

	@staticmethod
	def write_on_div(text: str, css_class: str = None):
		"""..."""
		css_class = f' class="{css_class}"' if css_class else ''
		st.markdown(
			f"""<div{css_class}>{text}</div>""",
			unsafe_allow_html=True)

	@staticmethod
	def write_on_p(text: str, css_class: str = None):
		"""..."""
		css_class = f' class="{css_class}"' if css_class else ''
		st.markdown(
			f"""<p{css_class}>{text}</p>""",
			unsafe_allow_html=True)

	@staticmethod
	def tag(tag: str, text: str = None, class_: str = None, style: str = None
			) -> str:
		"""..."""
		text = text if text else ''
		class_ = f' class="{class_}"' if class_ else ''
		style = f' style="{style}"' if style else ''
		return f"""<{tag}{class_}{style}>{text}</{tag}>"""

	@staticmethod
	def span_tag(text: str, css_class: str = None) -> str:
		"""..."""
		css_class = '' if not css_class else f' class="{css_class}"'
		return f"""<span{css_class}>{text}</span>"""

	@staticmethod
	def set_local_css(
			css_file: str = os.path.join(BASE_DIR, 'statics', 'style.css')
			) -> None:
		"""..."""
		with open(css_file) as f:
			st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

	@staticmethod
	def set_remote_css(
			url: str = 'https://fonts.googleapis.com/icon?family=Material+Icons'
			) -> None:
		"""..."""
		st.markdown(
			f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)
