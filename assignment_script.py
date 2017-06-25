import requests, browsercookie, re, os, easygui, UnRAR2
from pyunpack import Archive
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

assignment_id = easygui.enterbox(
	msg = 'Please insert the id of the assignment you wish to download\n\n*Use firefox',
	title = 'edu_download_helper',
	image = 'edu.PNG',
	strip = True, # will remove whitespace around whatever the user types in
	default = "") 

url = 'https://magshimim.edu20.org/teacher_dropbox_assignment/grading/' + assignment_id + '/'
cj = browsercookie.firefox()
page = requests.get(url, cookies=cj, verify=False)
get_student = lambda html: re.findall('/teacher_dropbox_assignment/grade(.*?)\"><span>', html, flags=re.DOTALL)
acurrances_list = get_student(page.content)
#create folder for assignments
folder_path = '../students_homework_' + assignment_id
if not os.path.exists(folder_path):
	os.makedirs(folder_path)
	
#create name dictionary
name_list = lambda html: re.findall('<a href=\"/user/show/(.*?)\">', html, flags=re.DOTALL)
names = name_list(page.content)
names_dic = {}
for name in names:
	no_comma_name = name[16:len(name)].replace(',', '_')
	no_space_name = no_comma_name.replace(' ', '')
	names_dic[name[:7]] = no_space_name

report = []
#get all assignments, in each assignment download zip file	
for accurance in acurrances_list:
	url = 'https://magshimim.edu20.org/teacher_dropbox_assignment/grade' + accurance
	page = requests.get(url, cookies=cj, verify=False)
	get_assignment = lambda html: re.findall('href=\'/files/(.*?)\'  target', html, flags=re.DOTALL)
	assignment = get_assignment(page.content)
	if len(assignment) == 0:
		pass
	else:
		url = 'https://magshimim.edu20.org/files/' + assignment[0]
		cur_name = "%s" %  names_dic.get(assignment[0][:7])
		
		page = requests.get(url, cookies=cj, verify=False)
		#download zip/rar files
		if (assignment[0][-4:] == '.zip' or assignment[0][-4:] == '.rar'):
			zip_file_path = folder_path + '/' + cur_name + assignment[0][-4:]
			zip_file = open(zip_file_path, 'wb')
			zip_file.write(page.content)
			zip_file.close()
		
			if not os.path.exists(folder_path + '/' + cur_name + '_extracted'):
				os.makedirs(folder_path + '/' + cur_name + '_extracted')
			#unpack zip files
			try:
				if(assignment[0][-4:] == '.rar'):
					rarc = UnRAR2.RarFile(zip_file_path)
					rarc.extract('*', folder_path + '/' + cur_name + '_extracted', True, True)
				else:
					Archive(zip_file_path).extractall(folder_path + '/' + cur_name + '_extracted')
				report.append(cur_name + ": Is ready\n")
				print cur_name + ": Is ready\n"
			except Exception as inst:
				report.append(cur_name + ": Failed\n")
				print cur_name + ": Failed\n"
		#other files
		else:
			if(assignment[0][-4:] == 'docx'):
				notzip_file = folder_path + '/' + cur_name + '.docx'
			else:
				notzip_file = folder_path + '/' + cur_name + assignment[0][-4:]
			notzip = open(notzip_file, 'wb')
			notzip.write(page.content)
			notzip.close()
			report.append(cur_name + ": Is ready\n")
			print cur_name + ": Is ready\n"
			
report.append("\n\nThank you for using edu_download_helper.\nFor bug reports or improvement ideas, please talk to your rakaz :)\n")
			
easygui.textbox(
	msg = 'download report',
	title = 'edu_download_helper',
	text = report
	) 
