const { app, BrowserWindow } = require('electron');
const path = require('path');
const { exec } = require('child_process');

// Function to create the Electron window
function createWindow() {
    const win = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    // Delay loading the window for 5 seconds to allow Flask to start
    setTimeout(() => {
        win.loadURL('http://127.0.0.1:5000'); // Load your Flask app URL after delay
    }, 5000); // Wait for 5 seconds
}

app.whenReady().then(() => {
    // Start the Flask server in the background using a Python command
    exec('python src/main/app.py', {
        cwd: path.join(__dirname, '..') // Navigate to the directory where app.py is located
    }, (err, stdout, stderr) => {
        if (err) {
            console.error(`Error starting Flask: ${err}`);
            return;
        }
        console.log(stdout); // Log Flask output
    });

    // Create the Electron window with the 5-second delay
    createWindow();

    app.on('activate', function () {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

// Quit the app when all windows are closed, except on macOS
app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
