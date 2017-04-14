from Managers import DocsetManager, ServerManager
from Views import DocsetManagementView, SettingsView, DocsetListView, DocsetView, DocsetIndexView, DocsetWebView
import ui
import threading

class PyDoc(object):
	def __init__(self):
		self.docset_manager = DocsetManager.DocsetManager('Images/icons', 'Images/types', ServerManager.ServerManager())
		self.main_view = self.setup_main_view()
		self.navigation_view = self.setup_navigation_view()
		self.management_view = self.setup_management_view()
		self.settings_view = self.setup_settings_view()
		
	def setup_navigation_view(self):
		nav_view = ui.NavigationView(self.main_view)
		return nav_view

	def setup_main_view(self):
		docsets = self.docset_manager.getDownloadedDocsets()
		main_view = DocsetListView.get_view(docsets, self.docset_selected_for_viewing)
		settings_button = ui.ButtonItem(title='Settings')
		settings_button.action = self.show_settings_view
		main_view.left_button_items = [settings_button]
		return main_view

	def setup_management_view(self):
		docsets = self.docset_manager.getAvailableDocsets()
		return DocsetManagementView.get_view(docsets, self.docset_manager.downloadDocset, self.docset_manager.getAvailableDocsets, self.docset_manager.deleteDocset, self.refresh_main_view_data)
	
	def refresh_main_view_data(self):
		docsets = self.docset_manager.getDownloadedDocsets() 
		DocsetListView.refresh_view(docsets)
				
	def setup_settings_view(self):
		return SettingsView.get_view(self.management_view)
		
	def show_settings_view(self, sender):
		self.navigation_view.push_view(self.settings_view)
	
	def docset_selected_for_viewing(self, docset):
		types = self.docset_manager.getTypesForDocset(docset)
		view = DocsetView.get_view(docset, types, self.docset_type_selected_for_viewing)
		self.navigation_view.push_view(view)
	
	def docset_type_selected_for_viewing(self, docset, type):
		indexes = self.docset_manager.getIndexesbyTypeForDocset(docset, type)
		view = DocsetIndexView.get_view(docset, indexes, self.docset_index_selected_for_viewing)
		self.navigation_view.push_view(view)
		
	def docset_index_selected_for_viewing(self, url):
		view = DocsetWebView.get_view(url)
		self.navigation_view.push_view(view)
	
	def update_memory(self):
		from Utilities import Memory
		import time
		while self.navigation_view.on_screen:
			self.navigation_view.name = str(Memory.get_memory_details()['free'])
			time.sleep(0.5)
			
			
if __name__ == '__main__':
	py = PyDoc()
	py.navigation_view.present(hide_title_bar=False)
	t = threading.Thread(target=py.update_memory)
	t.start()
	
