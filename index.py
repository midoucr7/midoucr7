
from PyQt5.QtWidgets import *  # importing Libreries!!!#
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType

import sys
import os
from os import path
import urllib.request
import pafy
from pafy import new
import youtube_dl
import humanize
import threading


FORM_CLASS ,_ = loadUiType(path.join(path.dirname(__file__), "main.ui"))  # PyQt5 FORM CLASSSSS its fixed all the time #

class MainApp(QMainWindow, FORM_CLASS):    # Creating the mainapp class!!!! #
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Ui()             ### convocate all Functions in the body fo the constructor __init__ ####
        self.Handel_Buttons()
        
        
                                   # bulding Functions #


    def Handel_Ui(self):                                                    # The UI function#
        self.setWindowTitle('Py_Downloader')
        self.setFixedSize(634, 318)



    def Handel_Buttons(self):  # buttons functions#
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_3.clicked.connect(self.Handel_Browse)
        self.pushButton_5.clicked.connect(self.Download_Youtube_Videos)
        self.pushButton_8.clicked.connect(self.Get_Youtube_Videos)
        self.pushButton_6.clicked.connect(self.Save_Browse)
        self.pushButton_7.clicked.connect(self.Playliste_Download)
        self.pushButton_4.clicked.connect(self.Save_Browse)

    def Handel_Browse(self):
        save_place = QFileDialog.getSaveFileName(self, caption= "Save as", directory= ".", filter= "All Files(*.*)")
        text = str(save_place)  # change to string#
        name = (text[2:].split(',')[0].replace("'" ,''))  # slicing to give us the diroctry of save_place #
        self.lineEdit_3.setText(name)  # show the directory in the browser line_edit#



    def Handel_Progress(self, blocknum, blocksize, totalsize):  # counting percent of download Function#
        read = blocknum * blocksize
        if totalsize > 0:
            percent = read * 100 / totalsize
            self.progressBar.setValue(percent)
            QApplication.processEvents()    ##For the app no repons ##




    def Download(self):
        url = self.lineEdit.text()
        save_location = self.lineEdit_3.text()
        try:
            urllib.request.urlretrieve(url, save_location, self.Handel_Progress)
        except Exception:
            QMessageBox.warning(self, "Download Error", "Your Download is Fieled")
            return
        QMessageBox.information(self, "Download is completed", "Your Download is Finished")
        self.progressBar.setValue(0)
        self.lineEdit.setText('')
        self.lineEdit_3.setText('')



    def Save_Browse(self):
        save = QFileDialog.getExistingDirectory(self, "Select Download directory")
        self.lineEdit_5.setText(save)
        self.lineEdit_4.setText(save)


    def Get_Youtube_Videos(self):
        video_link = self.lineEdit_6.text()
        v = pafy.new(video_link)
        st = v.allstreams                  #if no audio you just replace by v.streams#
        # print(v.title)
        # print(v.duration)
        # print(v.rating)
        # print(v.author)
        # print(v.length)
        # print(v.keywords)
        # print(v.thumb)
        # print(v.videoid)
        # print(v.viewcount)
        # print(st)
        for s in st:
            size = humanize.naturalsize(s.get_filesize())  # change Binnary to migabites#
            data = '{} {} {} {}'.format(s.mediatype ,s.quality, s.extension, size)
            self.comboBox.addItem(data)




    def Download_Youtube_Videos(self):
        video_link = self.lineEdit_6.text()
        savel_ocation = self.lineEdit_5.text()
        v = pafy.new(video_link)
        st = v.allstreams                                    #if no audio you just replace by v.streams#
        quality = self.comboBox.currentIndex()
        down = st[quality].download(filepath=savel_ocation,remux_audio=False)
        QMessageBox.information(self, "Download is completed", "Your Download is Finished")


    def Playliste_Download(self):
        playlist_url = self.lineEdit_2.text()
        save_location = self.lineEdit_4.text()
        if playlist_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid Playlist URL or save location")

        else:
            playlist = pafy.get_playlist(playlist_url)
            playlist_videos = playlist['items']

            self.lcdNumber_2.display(len(playlist_videos))

        os.chdir(save_location)
        if os.path.exists(str(playlist['title'])):
            os.chdir(str(playlist['title']))

        else:
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))

        current_video_in_download = 1
        quality = self.comboBox_2.currentIndex()


def main():
        app = QApplication(sys.argv)
        window = MainApp()
        window.show()
        app.exec_()
if __name__ == '__main__':
        main()

