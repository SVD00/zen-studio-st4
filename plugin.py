import sublime, sublime_plugin
from ctypes import c_char_p, c_void_p, cast, Structure
from ctypes.wintypes import DWORD, WPARAM
import win32gui, win32api

ULONG_PTR = WPARAM
WM_COPYDATA = 0x4A;

# https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-copydatastruct
class COPYDATASTRUCT(Structure):
	_fields_ = [
		('dwData', ULONG_PTR),
		('cbData', DWORD),
		('lpData', c_void_p)
	]

class Plugin:
	def __init__(self, view, message_type):
		"""
		Initialize the plugin

		:param view:			The view that contains the text to send to Zen Studio.
		:param message_type:	1 = GpcTab | 2 = BuildAndRun
		"""
		self.view = view
		self.type = message_type
		# Get all text from sublime text view
		self.text = view.substr(sublime.Region(0, self.view.size()))

	def run(self):
		# Get the Zen Studio handle(s)
		hwnd_list = self.find_zen_studio()

		# Convert text to bytes and cast into a pointer
		cmessage = c_char_p(self.text.encode())
		cmessagep = cast(cmessage, c_void_p)

		# Initialize Data Struct
		cds = COPYDATASTRUCT()
		cds.dwData = self.type
		cds.cbData = len(self.text)
		cds.lpData = cmessagep

		# Send message to all Zen Studio processes
		# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendmessage
		for hwnd in hwnd_list:
			win32api.SendMessage(hwnd, WM_COPYDATA, 0, cds)

	def find_zen_studio(self):
		"""
		Find the zen studio process by enumerating open windows.

		:return: list of handles to open windows that contain the text "Zen Studio"
		"""
		# list for HWND's
		list = []

		# Callback function
		def check_process(hwnd, ctx):
			if "Zen Studio" in win32gui.GetWindowText(hwnd):
				list.append(hwnd)

		# Enumerate all windows
		win32gui.EnumWindows(check_process, None)
		return list
