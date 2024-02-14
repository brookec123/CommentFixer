const vscode = require("vscode");
const path = require("path");
const { spawn } = require("child_process");

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
                // console.log(fileExtension)
                // Path to your Python script
                pythonScriptPath = path.join(__dirname, "//C//c_comments.py");
            }
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
            
            console.log("Author from settings:", getUserDefinedSettings());

            // Construct the command to execute the Python script with arguments
            let command = `python ${pythonScriptPath} --file ${currentlyOpenTabfilePath} --author "${getUserDefinedSettings()}"`;

            // Execute the Python script in a child process
            const pythonProcess = spawn(command, { shell: true });


            // Capture output from the child process
            // pythonProcess.stdout.on("data", (data) => {
            //     console.log(`Received data from Python script: ${data}`);
            // });

            pythonProcess.stderr.on("data", (data) => {
                console.error(`Error from Python script: ${data}`);
            });

            // Optionally, you can clear the terminal after a delay
            setTimeout(() => { vscode.commands.executeCommand("workbench.action.terminal.clear"); }, 2000);
            
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
