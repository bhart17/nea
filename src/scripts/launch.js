const { app, BrowserWindow } = require('electron');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        icon: `${app.getAppPath()}/src/assets/icon.png`,
        darkTheme: true,
        fullscreen: true,
        webPreferences: { sandbox: true },
        show: true,
        center: true
    })

    mainWindow.loadURL('http://localhost:8000/cache/index.html');

    //mainWindow.webContents.openDevTools()

    mainWindow.once('ready-to-show', () => {
        mainWindow.show()
    })

    mainWindow.on('closed', () => {
        mainWindow = null
    })
}

app.on('ready', createWindow)

app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') app.quit()
})

app.on('activate', function () {
    if (mainWindow === null) createWindow()
})