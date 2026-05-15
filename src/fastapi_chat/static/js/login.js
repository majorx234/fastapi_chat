import {httpPostFetch} from "./http_operation.js";
import "./forge-sha256.min.js";

function tokenEvent(token) {
    console.log("niy: token: " + token);
}
function logEvent(msg) {
    console.log("niy msg: " + msg);
}

function sendLogin() {
     let end_point_name = "login/login";
     let variable_context = "login: ";
     let username = document.getElementById("usernameInput").value;
     let password = document.getElementById("passwordInput").value;
     let hashed_password = forge_sha256(password + "salt29562");
     let json_data = {
         username: username,
         hashed_password: hashed_password
     };
     let response_handler = (response_text) => {
         let json_data = JSON.parse(response_text);
         let token = json_data["token"];
         tokenEvent(token);
         logEvent(variable_context + response_text);
     };
     let json_string = JSON.stringify(json_data);
     httpPostFetch(end_point_name, json_string, variable_context, response_handler, null, 'json');
}

document.getElementById("loginButton").onclick = () => {
    sendLogin();
};
