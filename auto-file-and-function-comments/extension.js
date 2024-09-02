const vscode = require("vscode");
const path = require("path");
const { spawn } = require("child_process");

// const userDefinedSettingVariableStrings = ["%file_name%", "%class_name%", "%method_name%", "%access_specifier%", "%author%", "%date%", "%parameter_name%", "%parameter_type%", "%return_type%"];

function getCUserDefinedSettings() {
    let userSettings = new Map();
    let separator = '\\~\\\`/~/';
    const config = vscode.workspace.getConfiguration("brookec.auto-file-and-function-comments.c.comment-writer");
    userSettings.set("author", config.get("author"));
    userSettings.set("date", config.get("date"));
    let additionalFileComments = config.get("additional-file-comments");
    if (Array.isArray(additionalFileComments)) {
        additionalFileComments = additionalFileComments.join(separator);
    } else {
        console.error("additional-file-comments is not an array");
    }
    userSettings.set("additional-file-comments", additionalFileComments);

    let additionalMethodComments = config.get("additional-method-comments");
    if (Array.isArray(additionalMethodComments)) {
        additionalMethodComments = additionalMethodComments.join(separator);
    } else {
        console.error("additional-method-comments is not an array");
    }
    userSettings.set("additional-method-comments", additionalMethodComments);

    let additionalADTComments = config.get("additional-adt-comments");
    if (Array.isArray(additionalADTComments)) {
        additionalADTComments = additionalADTComments.join(separator);
    } else {
        console.error("additional-adt-comments is not an array");
    }
    userSettings.set("additional-adt-comments", additionalADTComments);
    return userSettings;
}

function getJavaUserDefinedSettings() {
    let userSettings = new Map();
    let separator = '\\~\\\`/~/';
    const config = vscode.workspace.getConfiguration("brookec.auto-file-and-function-comments.java.comment-writer");
    userSettings.set("author", config.get("author"));
    userSettings.set("date", config.get("date"));
    let additionalFileComments = config.get("additional-file-comments");
    if (Array.isArray(additionalFileComments)) {
        additionalFileComments = additionalFileComments.join(separator);
    } else {
        console.error("additional-file-comments is not an array");
    }
    userSettings.set("additional-file-comments", additionalFileComments);

    let additionalMethodComments = config.get("additional-method-comments");
    if (Array.isArray(additionalMethodComments)) {
        additionalMethodComments = additionalMethodComments.join(separator);
    } else {
        console.error("additional-method-comments is not an array");
    }
    userSettings.set("additional-method-comments", additionalMethodComments);

    let additionalADTComments = config.get("additional-adt-comments");
    if (Array.isArray(additionalADTComments)) {
        additionalADTComments = additionalADTComments.join(separator);
    } else {
        console.error("additional-adt-comments is not an array");
    }
    userSettings.set("additional-adt-comments", additionalADTComments);
    return userSettings;
}

function getPythonUserDefinedSettings() {
    let userSettings = new Map();
    let separator = '\\~\\\`/~/';
    const config = vscode.workspace.getConfiguration("brookec.auto-file-and-function-comments.python.comment-writer");
    userSettings.set("author", config.get("author"));
    userSettings.set("date", config.get("date"));
    let additionalFileComments = config.get("additional-file-comments");
    if (Array.isArray(additionalFileComments)) {
        additionalFileComments = additionalFileComments.join(separator);
    } else {
        console.error("additional-file-comments is not an array");
    }
    userSettings.set("additional-file-comments", additionalFileComments);

    let additionalMethodComments = config.get("additional-method-comments");
    if (Array.isArray(additionalMethodComments)) {
        additionalMethodComments = additionalMethodComments.join(separator);
    } else {
        console.error("additional-method-comments is not an array");
    }
    userSettings.set("additional-method-comments", additionalMethodComments);

    let additionalADTComments = config.get("additional-adt-comments");
    if (Array.isArray(additionalADTComments)) {
        additionalADTComments = additionalADTComments.join(separator);
    } else {
        console.error("additional-adt-comments is not an array");
    }
    userSettings.set("additional-adt-comments", additionalADTComments);

    return userSettings;
}

// function getUserDefinedSettings() {
//     let userSettings = new Map();
//     let separator = '\\~\\\`/~/';
//     const config = vscode.workspace.getConfiguration("brookec.auto-file-and-function-comments.comment-writer");
//     userSettings.set("author", config.get("author"));
//     userSettings.set("date", config.get("date"));
//     let additionalFileComments = config.get("additional-file-comments");
//     if (Array.isArray(additionalFileComments)) {
//         additionalFileComments = additionalFileComments.join(separator);
//     } else {
//         console.error("additional-file-comments is not an array");
//     }
//     userSettings.set("additional-file-comments", additionalFileComments);

//     let additionalMethodComments = config.get("additional-method-comments");
//     if (Array.isArray(additionalMethodComments)) {
//         additionalMethodComments = additionalMethodComments.join(separator);
//     } else {
//         console.error("additional-method-comments is not an array");
//     }
//     userSettings.set("additional-method-comments", additionalMethodComments);

//     let additionalADTComments = config.get("additional-adt-comments");
//     if (Array.isArray(additionalADTComments)) {
//         additionalADTComments = additionalADTComments.join(separator);
//     } else {
//         console.error("additional-adt-comments is not an array");
//     }
//     userSettings.set("additional-adt-comments", additionalADTComments);
//     return userSettings;
// }

function generateCommand(pythonScriptPath, currentlyOpenTabfilePath, userSettings) {
    let command = `python ${pythonScriptPath} --file ${currentlyOpenTabfilePath}`;
    userSettings.forEach((value, key) => {
        command += ` --${key} \"${value}\"`
    });
    return command;
}

function activate(context) {
    let disposableWriter = vscode.commands.registerCommand("auto-file-and-function-comments.comment-writer", () => {
        const activeTextEditor = vscode.window.activeTextEditor;

        if (activeTextEditor) {
            var currentlyOpenTabfilePath = vscode.window.activeTextEditor.document.fileName;
            var fileName = vscode.window.activeTextEditor.document.fileName;
            var fileExtension = fileName.substring(fileName.lastIndexOf(".") + 1, fileName.length) || fileName;
            var pythonScriptPath = "";

            // Construct the command to execute the Python script with arguments
            let command = "";

            if (fileExtension == "c" || fileExtension == "cpp" || fileExtension == "h" || fileExtension == "hpp") {
                // Path to your Python script
                pythonScriptPath = path.join(__dirname, "//C//c_comments.py");
                command = generateCommand(pythonScriptPath, currentlyOpenTabfilePath, getCUserDefinedSettings());
                console.log(command);
            }
            else if (fileExtension == "java") {
                // Path to your Python script
                pythonScriptPath = path.join(__dirname, "//Java//java_comments.py");
                command = generateCommand(pythonScriptPath, currentlyOpenTabfilePath, getJavaUserDefinedSettings());
            }
            else if (fileExtension == "py") {
                // Path to your Python script
                pythonScriptPath = path.join(__dirname, "//Python//python_comments.py");
                command = generateCommand(pythonScriptPath, currentlyOpenTabfilePath, getPythonUserDefinedSettings());
            }

            // Execute the Python script in a child process
            const pythonProcess = spawn(command, { shell: true });

            // Capture output from the child process
            pythonProcess.stdout.on("data", (data) => {
                console.log(`Received data from Python script: ${data}`);
            });

            pythonProcess.stderr.on("data", (data) => {
                console.error(`Error from Python script: ${data}`);
            });

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
