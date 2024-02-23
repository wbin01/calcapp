#!/usr/bin/env python3
import os
import pathlib

import PIL
import streamlit as st

from modules.streamlitextras import StreamlitExtras

BASE_DIR = pathlib.Path(__file__).resolve().parent


st.set_page_config(
	page_title='Calc App',
	page_icon=PIL.Image.open(os.path.join(BASE_DIR, 'statics', 'favicon.png')),
	layout='centered',  # centered, wide
	initial_sidebar_state='collapsed',  # auto expanded collapsed
	menu_items={
		'Get Help': 'https://www.extremelycoolapp.com/help',
		'Report a bug': 'https://www.extremelycoolapp.com/bug',
		'About': '# This is a header. This is an *extremely* cool app!'})


class CalcApp(object):
	"""..."""
	def __init__(self) -> None:
		"""..."""
		super().__init__()
		self.st = StreamlitExtras()

	def main(self) -> None:
		"""..."""
		self.st.disable_sidebar()
		if 'clicked' not in st.session_state:
			st.session_state.history = []
			st.session_state.clicked = ''
			st.session_state.result = ''
			st.session_state.emoji = '🤔'

		_, center_column, _ = st.columns([1, 2, 1])
		with center_column:
			with st.container(border=True):
				self.__render_history()
				self.__render_operation_area()
				self.__render_buttons()

	@staticmethod
	def __on_history() -> None:
		if st.session_state.history:
			st.session_state.clicked = st.session_state.history[-1][0]
			st.session_state.history = st.session_state.history[:-1]

	@staticmethod
	def __erase_last_clicked_value() -> None:
		if st.session_state.clicked:
			st.session_state.clicked = st.session_state.clicked[:-1]

	@staticmethod
	def __treat_last_clicked_value() -> None:
		signals = ['-', '.', '=', '+', '*']
		if len(st.session_state.clicked) == 1:
			if st.session_state.clicked in signals[1:] + ['/']:
				st.session_state.clicked = st.session_state.clicked[:-1]

		elif len(st.session_state.clicked) > 1:
			last = st.session_state.clicked[-1]
			previous = st.session_state.clicked[-2]

			if st.session_state.clicked.endswith('///'):
				st.session_state.clicked = st.session_state.clicked[:-1]

			elif (last in signals and previous in signals or
					st.session_state.clicked.endswith('///')):
				st.session_state.clicked = st.session_state.clicked[:-2] + last

	@staticmethod
	def __has_signal_in_values() -> bool:
		sg = ['+', '-', '*', '/']
		if st.session_state.clicked and st.session_state.clicked[-1] not in sg:
			for signal in sg:
				if signal in st.session_state.clicked:
					return True
		return False

	def __on_click(self, *value) -> None:
		value = ''.join(value)
		st.session_state.emoji = '🤔'
		st.session_state.result = ''

		if value == '<':
			self.__erase_last_clicked_value()
		elif value == '=':
			self.__result()
		elif value == 'C':
			st.session_state.clicked = ''
		elif value == 'back':
			self.__on_history()
		else:
			st.session_state.clicked += value
			self.__treat_last_clicked_value()

	def __render_buttons(self) -> None:
		button_num = [
			str(x) for x in range(9, 0, -1)] + [
			'(', '0', ')', '=', '.', '/', '*', '-', '+', 'C', '<']

		for row in range(4):
			for col, num in zip(st.columns(5), range(1, 6)):
				with col:
					key = button_num.pop() if (
						num % 4 == 0 or num % 5 == 0) else button_num.pop(0)
					
					st.button(
						key + '&nbsp;' if key != '<' else '←',
						key=key,
						on_click=self.__on_click,
						args=key,
						type='secondary' if key.isdigit() else 'primary',
						use_container_width=True)

	def __render_history(self) -> None:
		text = ''
		for history in st.session_state.history:
			text = self.st.tag(
				'p',
				self.st.tag('span', f'{history[0]}', class_='history-values')
				+ ' = ' +
				self.st.tag('span', history[1], class_='history-result')
				) + text
		st.markdown(
			self.st.tag('div', text, class_='vscrollbar'),
			unsafe_allow_html=True)

	def __render_operation_area(self) -> None:
		result_col, back_col = st.columns([4, 1])
		with result_col:
			cla = 'result' if st.session_state.result else 'operations'

			txt = f'{st.session_state.emoji}   {st.session_state.clicked}'
			if st.session_state.result:
				txt = f'{st.session_state.emoji}   {st.session_state.result}'

			st.markdown(
				self.st.tag('div', txt, class_=cla, style='margin-top: 7px;'),
				unsafe_allow_html=True)
		
		with back_col:
			st.button('<<', key='back', on_click=self.__on_click,
				args='back', use_container_width=True)

	def __result(self) -> None:
		if st.session_state.clicked and self.__has_signal_in_values():
			try:
				result = str(eval(st.session_state.clicked.lstrip('0')))
				if len(result) > 1 and result[-2:] == '.0':
					result = result[:-2]
			except Exception as err:
				st.session_state.clicked = '❌'
				st.session_state.emoji = '😮 Formato incorreto!'
			else:
				st.session_state.history.append(
					(st.session_state.clicked, result))
				st.session_state.clicked = result
				st.session_state.result = result
				st.session_state.emoji = '😌'


if __name__ == '__main__':
	app = CalcApp()
	app.main()
