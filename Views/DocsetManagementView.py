
import ui

class DocsetManagementView (object):
	def __init__(self, docsets, download_action, refresh_docsets_action):
		self.data = docsets
		self.download_action = download_action
		self.refresh_docsets_action = refresh_docsets_action
		
		
	def tableview_did_select(self, tableview, section, row):
		pass
		
	def tableview_number_of_sections(self, tableview):
		return 1
		
	def tableview_number_of_rows(self, tableview, section):
		return len(self.data)
		
	def tableview_cell_for_row(self, tableview, section, row):
		status = self.data[row]['status']
		cell = ui.TableViewCell('subtitle')
		cell.text_label.text = self.data[row]['name']
		cell.detail_text_label.text = status
		if not self.data[row]['image'] == None:
			cell.image_view.image = self.data[row]['image']
		iv = self.__getDetailButtonForStatus(status, cell.height, self.action, self.data[row])
		iv.x = cell.content_view.width - (iv.width * 1.5)
		iv.y = (cell.content_view.height) - (iv.height * 1.05)
		iv.flex = 'L'
		cell.content_view.add_subview(iv)
		cell.selectable = False
		return cell
		
	def __getDetailImageForStatus(self, status):
		if status == 'online' or status == 'updateAvailable':
			return 'iob:ios7_cloud_download_outline_24'
		else:
			return 'iob:ios7_close_outline_24'
			
	def __getDetailButtonForStatus(self, status, height, action, row):
		img = ui.Image.named(self.__getDetailImageForStatus(status))
		button = ui.Button()
		button.image = img
		size = img.size
		ratio = size.y / size.x
		button.height = height * 0.9
		button.width = button.height * ratio
		ca = CustomAction(button)
		ca.action = self.action
		ca.row = row
		button.action = ca
		return button
		
	def action(self, sender):
		self.download_action(sender.action.row)
		self.refresh()
	
	def refresh(self):
		self.data = self.refresh_docsets_action()
		tv.reload()
		
class CustomAction(object):
	def __init__(self, parent):
		self.obj = parent
		self.action = self.real_action
		self.row = None
		
	def __call__(self, sender):
		return self.action(sender)
		
	def real_action(self, sender):
		print('Did you need to set the action?')

tv = ui.TableView()
def get_view(docsets, download_action, refresh_docsets_action):
	w,h = ui.get_screen_size()
	tv.width = w
	tv.height = h
	tv.flex = 'WH'
	tv.name = 'Docsets'
	data = DocsetManagementView(docsets, download_action, refresh_docsets_action)
	tv.delegate = data
	tv.data_source = data
	return tv
	
if __name__ == '__main__':
	view = get_view([{'name':'test','status':'online'},{'name':'test2','status':'downloaded'}])
	view.present()
