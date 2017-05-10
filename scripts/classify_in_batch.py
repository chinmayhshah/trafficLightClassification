import argparse, os

#Add folder name here to classify traffic signs
# list_folder = ["30","50","MEN_WORK","PEDES","SPLIT_RIGHT","STOP","TURN_RIGHT","ROUND_ABOUT"]
list_folder = ["30", "50", "MEN_WORK", "ROUND_ABOUT"]

#Change the solver here : SGD, ADA or NAG
SOLVER = "SGD"


def add_message(file_name, MESSAGE):
    # MESSAGE="With GPU \n"
    f = open(file_name, 'a');
    f.write(MESSAGE)
    f.close();


def iterate_sign_classify():
    for every in list_folder:
        add_message("output_new.txt", "\n" + every + " Classification")

        FOLDER_AT = every
        add_message("output_new.txt", "\n# With  GPU Overclocked \n")
        folder = "/home/ubuntu/aca-project_data/classify_signs/" + FOLDER_AT + "/"
        add_message("output_new.txt", "\nEPoch 1\n")

        COMMAND = "python ~/caffe/python/use_archive.py ~/aca-project_data/" + SOLVER + "/1.tar.gz ~/aca-project_data/classify_signs/" + FOLDER_AT
        classify_all_images(folder, COMMAND, 0)
        add_message("output_new.txt", "#\n EPoch 6\n")
        COMMAND = "python ~/caffe/python/use_archive.py ~/aca-project_data/" + SOLVER + "/6.tar.gz ~/aca-project_data/classify_signs/" + FOLDER_AT
        classify_all_images(folder, COMMAND, 0)
        add_message("output_new.txt", "#\n EPoch 13\n")
        COMMAND = "python ~/caffe/python/use_archive.py ~/aca-project_data/" + SOLVER + "/13.tar.gz ~/aca-project_data/classify_signs/" + FOLDER_AT
        classify_all_images(folder, COMMAND, 0)


'''
        Add_message("output_new.txt","#\n Without GPU\n") 
    	folder = "/home/ubuntu/aca-project_data/classify_signs/"+FOLDER_AT+"/" 
	    Add_message("output_new.txt","#\n EPoch 1\n")	
       	COMMAND = "python ~/caffe/python/use_archive.py ~/aca-project_data/"+SOLVER+"/1.tar.gz ~/aca-project_data/classify_signs/"+FOLDER_AT
       	classify_all_images(folder,COMMAND,1)
	    Add_message("output_new.txt","#\n EPoch 6\n")
       	COMMAND = "python ~/caffe/python/use_archive.py ~/aca-project_data/"+SOLVER+"/6.tar.gz ~/aca-project_data/classify_signs/"+FOLDER_AT
       	classify_all_images(folder,COMMAND,1)
	    Add_message("output_new.txt","#\n EPoch 13\n")
       	COMMAND = "python ~/caffe/python/use_archive.py ~/aca-project_data/"+SOLVER+"/13.tar.gz ~/aca-project_data/classify_signs/"+FOLDER_AT
       	classify_all_images(folder,COMMAND,1)
'''


def classify_all_images(directory, COMMAND, GPU):
    print directory
    for file_name in os.listdir(directory):
        if (file_name.endswith(".png")):
            COMMAND_EXE = COMMAND + "/" + file_name
            if (GPU):
                COMMAND_EXE = COMMAND_EXE + " --nogpu"
            print COMMAND_EXE
            os.system(COMMAND_EXE)

        else:
            print "No such file"


if __name__ == "__main__":
    iterate_sign_classify()
