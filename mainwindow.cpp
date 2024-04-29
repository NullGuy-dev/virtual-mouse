#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include "QPushButton"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    connect(ui->open, &QPushButton::clicked, this, &MainWindow::Start);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::Start() {
    system("python vouse.py");
}
