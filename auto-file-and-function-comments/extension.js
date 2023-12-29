const vscode = require('vscode');
const path = require('path');
const cp = require('child_process');

function activate(context) {
    let disposable = vscode.commands.registerCommand('auto-file-and-function-comments.comment-writer', () => {
        const activeTextEditor = vscode.window.activeTextEditor;

        if (activeTextEditor) {
            var currentlyOpenTabfilePath = vscode.window.activeTextEditor.document.fileName;
            var fileType = vscode.window.activeTextEditor.document.languageId;
            var pythonScriptPath = "";
            if (fileType == "c" || fileType == "cpp")
            {
                // Path to your Python script
                pythonScriptPath = path.join(__dirname, '//C//c_comments.py');
            }
            else if (fileType == "java")
            {
                // Path to your Python script
                pythonScriptPath = path.join(__dirname, '//Java//java_comments.py');
            }
            else if(fileType == "python")
            {
                // Path to your Python script
                pythonScriptPath = path.join(__dirname, '//Python//python_comments.py');
            }
            var firstArg = "--file "+currentlyOpenTabfilePath;
            let config  = vscode.workspace.getConfiguration('auto-file-and-function-comments');
            var secondArg = "--author \"" + config.get('author', "First Last") + "\"";
            // Run the Python script
            let command = 'python ' + " " + pythonScriptPath + " " +firstArg + " " +secondArg;
            let terminalWindow = vscode.window.createTerminal("Comment Editor");
            terminalWindow.sendText(command);
            setTimeout(() => { terminalWindow.sendText("cls"); }, 2000);

            
        } else {
            vscode.window.showInformationMessage('No active editor found.');
        }
    });

    context.subscriptions.push(disposable);
}

function deactivate() {
    // Cleanup logic, if any
}

module.exports = {
    activate,
    deactivate
};
