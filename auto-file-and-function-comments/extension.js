const vscode = require("vscode");
const path = require("path");

function getUserDefinedSettings() {
    const config = vscode.workspace.getConfiguration("brookec.auto-commenter.comment-writer");
    const author = config.get("author");
    return author;
}

function activate(context) {
    let disposableWriter = vscode.commands.registerCommand("auto-commenter.comment-writer", () => {
        const activeTextEditor = vscode.window.activeTextEditor;

        if (activeTextEditor) {
            var currentlyOpenTabfilePath = vscode.window.activeTextEditor.document.fileName;
            var fileName = vscode.window.activeTextEditor.document.fileName;
            var fileExtension = fileName.substring(fileName.lastIndexOf(".")+1, fileName.length) || fileName;
            var pythonScriptPath = "";
            if (fileExtension == "c" || fileExtension == "cpp" || fileExtension == "h" || fileExtension == "hpp")
            {
                // Path to your Python script
                pythonScriptPath = path.join(__dirname, "//C//c_comments.py");
            }
            // else if (fileExtension == "cpp" || fileExtension == "h" || fileExtension == "hpp")
            // {
            //     // Path to your Python script
            //     pythonScriptPath = path.join(__dirname, "//CPP//cpp_comments.py");
            // }
            else if (fileExtension == "java")
            {
                // Path to your Python script
                pythonScriptPath = path.join(__dirname, "//Java//java_comments.py");
            }
            else if(fileExtension == "py")
            {
                // Path to your Python script
                pythonScriptPath = path.join(__dirname, "//Python//python_comments.py");
            }
            var firstArg = "--file "+currentlyOpenTabfilePath;
            var secondArg = "--author \"" + getUserDefinedSettings() + "\"";
            
            console.log("Author from settings:", getUserDefinedSettings());
            // Run the Python script
            let command = "python " + " " + pythonScriptPath + " " +firstArg + " " +secondArg;
            let terminalWindow = vscode.window.createTerminal("Auto Commenter");
            terminalWindow.sendText(command);
            setTimeout(() => { terminalWindow.sendText("cls"); }, 2000);

            
        } else {
            vscode.window.showInformationMessage("No active editor found.");
        }
    });

    context.subscriptions.push(disposableWriter);
}

function deactivate() {
    // Cleanup logic, if any
}

module.exports = {
    activate,
    deactivate
};