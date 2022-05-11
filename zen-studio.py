import sublime, sublime_plugin
from .plugin import Plugin

# view.run('send_to_studio')
class SendToStudioCommand(sublime_plugin.TextCommand):
	def run(self, edit, message_type):
		plugin = Plugin(self.view, message_type)
		plugin.run()