import autoNotationView
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PIL import Image
import os
import csv
import sys

class AutoNotationCore :

    def __init__(self) :
        self.view = None
        self.directory  = ""
        self.imageWithCropPath = ""
        self.imageWithCrop = []
        self.annotationCSV = []
        self.currentImageIndex = 0

    def setView (self, view) :
        self.view = view

    def tapOpen(self, fname) :
        self.imageWithCropPath = fname[0]
        if self.imageWithCropPath != "" :
            self.directory = os.path.dirname(self.imageWithCropPath)
            self.openCSV(self.imageWithCropPath, self.imageWithCrop)
            self.checkFolderCropExist()

    def openCSV (self, path, variable) :
        with open(path) as file:
            reader = csv.DictReader(file)
            for row in reader : variable.append(dict(row))

    def checkFolderCropExist(self) :
        if os.path.exists(self.directory+"\\crops") :
            print("Crops Folder exists")
            self.checkAnnotationCSVExist()
        else :
            print("Crops Folder doesn't exist")
            self.createCrops()

    def checkAnnotationCSVExist(self) :
        if os.path.exists(self.directory+"\\annotations.csv") :
            print("annotations.csv file exists")
            self.reCreateCrops()
            self.annotationTime()
        else :
            print("annotation.csv file doesn't exist")

    def createCrops(self) :
        # create missing files
        os.mkdir(self.directory+"\\crops")

        # create Crops
        with open(self.directory+"\\annotations.csv", "w", newline ='') as file:
            writer = csv.writer(file)
            writer.writerow(["imagePath","label"])
            paths = []
            for i, image in enumerate(self.imageWithCrop) :
                path = "{}\\crops\\image{}.jpg".format(self.directory,self.formattedIndex(i,4))
                paths.append([path])
                im = Image.open(image["pathImage"])
                imageCropped = im.crop((int(image["x1"]), int(image["y1"]), int(image["x2"]), int(image["y2"])))
                imageCropped.save(path)
            writer.writerows(paths)
        self.annotationTime()

    def reCreateCrops(self) :
        cropAnnot = []
        self.openCSV(self.directory+"\\annotations.csv", cropAnnot)
        for i in range(len(cropAnnot)) : cropAnnot[i] = [cropAnnot[i]["imagePath"], cropAnnot[i]["label"]]
        if len(cropAnnot) < len(self.imageWithCrop) :
            with open(self.directory+"\\annotations.csv", "w", newline ="") as file :
                writer = csv.writer(file)
                writer.writerow(["imagePath","label"])
                for i in range(len(cropAnnot), len(self.imageWithCrop)) :
                    path = "{}\\crops\\image{}.jpg".format(self.directory,self.formattedIndex(i,4))
                    cropAnnot.append([path])
                    im = Image.open(self.imageWithCrop[i]["pathImage"])
                    imageCropped = im.crop((int(self.imageWithCrop[i]["x1"]), int(self.imageWithCrop[i]["y1"]), int(self.imageWithCrop[i]["x2"]), int(self.imageWithCrop[i]["y2"])))
                    imageCropped.save(path)
                writer.writerows(cropAnnot)

    def formattedIndex(self, index, size) :
        index = str(index)
        while len(index) < size :
            index = "0" + index
        return index

    def annotationTime(self) :
        self.openCSV(self.directory+"\\annotations.csv", self.annotationCSV)

        #research the begining (if it is a reloading)
        for i, image in enumerate(self.annotationCSV) :
            if image["label"] == None or image["label"] == '':
                self.currentImageIndex = i
                break
        self.showAnnotation()

    def showAnnotation(self) :
        self.view.showImage(self.annotationCSV[self.currentImageIndex]["imagePath"])
        self.view.changeAvancementLabel("n°{} / {}".format(self.currentImageIndex+1, len(self.annotationCSV)))
        self.view.changeAnnotationLabel(self.annotationCSV[self.currentImageIndex]["label"])

    def tapOnPrevButton (self) :
        if self.currentImageIndex - 1 >= 0 :
            self.currentImageIndex -= 1
            self.showAnnotation()

    def tapOnNextButton(self) :
        if self.currentImageIndex + 1 < len(self.annotationCSV) :
            self.currentImageIndex += 1
            self.showAnnotation()

    def receiveAnnotation(self, annot) :
        self.annotationCSV[self.currentImageIndex]["label"] = annot
        self.tapOnNextButton()
        self.showAnnotation()
        if self.view :
            self.view.resetAnnotationInput()
        self.saveAnnotation()

    def goToImage(self, index) :
        if index > 0 and index < len(self.annotationCSV)+1 :
            self.currentImageIndex = index - 1
            self.showAnnotation()

    def saveAnnotation(self) :
        if len(self.annotationCSV) > 0 :
            with open(self.directory+"\\annotations.csv", "w",newline='') as file :
                print("try to save")
                writer = csv.DictWriter(file, fieldnames = list(self.annotationCSV[0].keys()))
                writer.writeheader()
                writer.writerows(self.annotationCSV)

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    core = AutoNotationCore()
    ui = autoNotationView.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.setCore(core)
    sys.exit(app.exec_())
